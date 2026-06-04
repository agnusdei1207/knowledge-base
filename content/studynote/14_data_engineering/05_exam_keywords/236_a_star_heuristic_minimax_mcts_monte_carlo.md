---
title: "236. A* 휴리스틱 (Heuristic) 미니맥스 (Minimax) MCTS (Monte Carlo Tree Search)"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: A*([A-Star](/studynote/10_ai/01_ai_basics/017_a_star_algorithm/)) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 함수 h(n)을 이용해 최단 경로를 효율적으로 탐색하며, [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/)([Minimax](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/))는 게임 트리에서 상대의 최선과 자신의 최선을 교차 선택해 최적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 찾는다.
> 2. **가치**: [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/)(Monte Carlo Tree Search)는 경우의 수가 폭발적으로 많은 바둑·체스에서 무작위 시뮬레이션 통계를 활용해 완전 탐색 없이 강력한 수를 선택하며, AlphaGo의 핵심 엔진이다.
> 3. **판단 포인트**: 탐색 공간 크기와 실시간 요건에 따라 [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/)/[DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)(작은 공간)->A*(경로 찾기)->알파-베타(게임 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))->[MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/)(복잡 게임) 순으로 방법론을 선택한다.

## Ⅰ. 개요 및 필요성

### 탐색(Search) 문제의 본질

AI가 해결해야 하는 많은 문제는 <strong>상태 공간(<a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a> Space) 탐색</strong>으로 표현된다: 현재 상태에서 목표 상태까지 최적 경로를 찾는 것이다.

| 문제 | 상태 | 행동 | 목표 |
|:---|:---|:---|:---|
| 경로 찾기 | 현재 위치 | 이동 방향 | 목적지 도달 |
| 바둑 | 현재 돌 배치 | 돌 놓기 | 승리 |
| 퍼즐 (8-Puzzle) | 타일 배치 | 타일 이동 | 정렬 완성 |
| 게임 나무 | 게임 상태 | 플레이어 이동 | 최대 점수 |

탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 효율성은 <strong><a href="/studynote/08_algorithm_stats/01_basics/002_time_complexity/">시간 복잡도</a></strong>와 <strong>최적성(Optimality)</strong>의 트레이드오프로 결정된다.

📢 **섹션 요약 비유**: 탐색 문제는 미로 찾기다. BFS는 모든 방향을 동시에 확인하고, DFS는 한 방향으로 끝까지 가보며, A*는 "출구가 저 방향일 것 같다"는 직관으로 효율적으로 찾아간다.

## Ⅱ. 아키텍처 및 핵심 원리

### 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 탐색 방식 | 최적성 | 시간복잡도 | 메모리 | 특징 |
|:---|:---|:---:|:---:|:---:|:---|
| [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) ([너비 우선 탐색](/studynote/08_algorithm_stats/03_graph_search/035_bfs/)) | 레벨 순서 | ✅ (비가중) | O(b^d) | 높음 | 최단 홉 보장 |
| [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) ([깊이 우선 탐색](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)) | 깊이 방향 | ❌ | O(b^m) | 낮음 | 무한 루프 위험 |
| [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) | 비용 우선 | ✅ (가중) | O((V+E)logV) | 높음 | 음의 간선 불가 |
| **A*** | 비용+[휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) | ✅ (허용적 h) | O(b^d) | 높음 | 최단 경로 효율적 |
| [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/) ([Minimax](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/)) | 게임 트리 전체 | ✅ | O(b^m) | 낮음 | 상대 최적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 가정 |
| [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) | 몬테카를로 샘플링 | 근사 | O(시뮬레이션 수) | 중간 | 복잡 게임에 강력 |

### A* [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([A-Star Algorithm](/studynote/08_algorithm_stats/03_graph_search/038_a_star_algorithm/))

```
평가 함수: f(n) = g(n) + h(n)

  g(n): 시작 노드에서 n까지의 실제 비용 (알려진 값)
  h(n): n에서 목표까지의 추정 비용 (휴리스틱)
  f(n): 경로 전체 예상 비용

허용적 휴리스틱 (Admissible Heuristic):
  h(n) ≤ h*(n)  (실제 비용 이하)
  -> 과소 추정 -> 최적 경로 보장

대표 휴리스틱:
  맨하탄 거리: |x1-x2| + |y1-y2|  (격자 이동)
  유클리드 거리: √((x1-x2)^ + (y1-y2)^)  (직선 이동)
```

**A* 탐색 과정 ([ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램)**
```
  S = 시작, G = 목표, 숫자 = g(n), 괄호 = h(n)

  S --3--> A --4--> G
  |       (4)      (0)
  |(7)
  +--5--> B --2--> C --1--> G
         (3)      (1)

  A*가 선택하는 경로:
    S->A: f = g(3)+h(4) = 7
    S->B: f = g(5)+h(3) = 8
    -> S->A 먼저 탐색
    A->G: f = g(7)+h(0) = 7  <- 최적!
```

### [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/) ([Minimax](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/)) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

2인 제로섬 게임에서 자신은 점수를 최대화(MAX), 상대는 최소화(MIN)한다고 가정하고 게임 트리 전체를 탐색한다.

```
                  루트 (내 차례: MAX)
                 /         \
             [3]             [5]
            /   \           /   \
MAX ->    [3]   [12]      [8]   [5]
         / \   / \       / \   / \
MIN ->   3  5 12  2     8  9  5   7
                                     <- 단말 노드 (점수)

알파-베타 가지치기 (Alpha-Beta Pruning):
  MAX 노드: α = 현재 최대값
  MIN 노드: β = 현재 최소값

  β ≤ α이면 해당 가지 탐색 중단 (가지치기)
  -> 최악 O(b^m) -> 최적 O(b^(m/2)) 개선
```

### [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) (Monte Carlo Tree Search) 4단계

AlphaGo에서 핵심적으로 사용된 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

```
+------------------------------------------------------------+
|                MCTS 4단계 반복 루프                          |
|                                                            |
|  1. 선택 (Selection)                                       |
|     UCT 공식으로 가장 유망한 노드 선택                        |
|     UCT(n) = Q(n)/N(n) + C × √(ln(N_parent)/N(n))         |
|                 탐욕         탐색 보너스                     |
|                                                            |
|  2. 확장 (Expansion)                                       |
|     선택된 노드에서 새 자식 노드 추가                         |
|                                                            |
|  3. 시뮬레이션 (Simulation/Rollout)                         |
|     무작위 혹은 정책 기반으로 게임 끝까지 플레이               |
|     결과: 승(+1) / 패(-1) / 무(0)                           |
|                                                            |
|  4. 역전파 (Backpropagation)                               |
|     시뮬레이션 결과를 루트까지 역방향으로 업데이트              |
|     N(n) += 1, Q(n) += 결과                                |
|                                                            |
|  -> 수천~수만 번 반복 후 방문 횟수 가장 많은 수 선택            |
+------------------------------------------------------------+
```

📢 **섹션 요약 비유**: MCTS는 미로에서 길을 찾을 때 "많이 탐험해서 자주 목적지에 도달한 경로"를 선택하는 방법이다. 개별 탐험은 무작위이지만 통계가 쌓이면 최선의 길이 드러난다.

## Ⅲ. 비교 및 연결

### A* vs [Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) 핵심 차이

```
다익스트라 (Dijkstra):
  모든 방향을 균등하게 탐색
  -> 목표 방향을 모름

A* 알고리즘:
  휴리스틱으로 목표 방향 편향 탐색
  -> 훨씬 빠르게 목표 도달

탐색 영역 비교 (격자 맵):
  다익스트라: 원형으로 전방향 탐색 (넓음)
  A*:         방향성 있는 탐색 (좁음, 효율적)
```

### [알파-베타 가지치기](/studynote/10_ai/01_ai_basics/020_alpha_beta_pruning/) 효과

| 조건 | 시간복잡도 | 비고 |
|:---|:---:|:---|
| [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) 없는 [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/) | O(b^m) | b=분기, m=깊이 |
| 최악 알파-베타 | O(b^m) | [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) 효과 없음 |
| 평균 알파-베타 | O(b^(3m/4)) | 무작위 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) |
| **최적 알파-베타** | **O(b^(m/2))** | **최선 순서 정렬** |

바둑의 경우 b≈250, m≈150이면 완전 탐색이 불가능 -> [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) + 신경망 필수

### AlphaGo 구조 ([MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) + 딥러닝)

```
+---------------------------------------------+
|              AlphaGo (2016)                  |
|                                             |
|  정책 네트워크 (Policy Network)              |
|  -> 다음 수 확률 분포 예측 (MCTS 선택 안내)  |
|                                             |
|  가치 네트워크 (Value Network)              |
|  -> 현재 상태 승률 예측 (시뮬레이션 대체)    |
|                                             |
|  MCTS + Policy + Value 통합                 |
|  -> 이세돌 9단 4:1 승리                     |
+---------------------------------------------+
```

📢 **섹션 요약 비유**: [알파-베타 가지치기](/studynote/10_ai/01_ai_basics/020_alpha_beta_pruning/)는 미리 "이 길은 절대 최선이 될 수 없다"고 판단해 탐색을 건너뛰는 것이다. 체스 선수가 "이 수는 분명 질 것 같으니 생각도 안 해"라고 하는 것과 같다.

## Ⅳ. 실무 적용 및 기술사 판단

### 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 기준

```
문제 유형별 알고리즘 선택:

  경로 찾기 (가중 그래프):     A* (최단 경로 보장, 효율적)
  경로 찾기 (비가중 그래프):   BFS (최소 홉 보장)
  2인 게임 (소규모):           미니맥스 + 알파-베타
  2인 게임 (바둑·대규모):      MCTS (+신경망)
  최단 거리 (음의 가중치):     벨만-포드 (Bellman-Ford)
  전체 최단 경로:              플로이드-워셜 (Floyd-Warshall)
```

### 실무 응용 사례

| 분야 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 응용 |
|:---|:---|:---|
| 자율주행 경로 계획 | A* / D* | 실시간 장애물 회피 경로 |
| 게임 NPC [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/) + 알파-베타 | 체스·장기 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| 바둑 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) + 딥러닝 | AlphaGo, KataGo |
| 물류 최적화 | A* + [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) | 배송 경로 최적화 |
| [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 네트워크 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) | [OSPF](/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |

📢 **섹션 요약 비유**: A*는 "내비게이션 앱"처럼 목적지 방향을 알고 효율적으로 길을 찾는다. MCTS는 "바둑 고수"처럼 수천 번의 상상 대국으로 최선의 수를 고른다.

## Ⅴ. 기대효과 및 결론

### 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 (동일 문제)

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 탐색 노드 수 | 최적 경로 보장 | 시나리오 |
|:---|:---:|:---:|:---|
| [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) | 1,000 | ✅ | 단순 격자 맵 |
| [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) | 800 | ✅ | 가중 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **A*** | **150** | ✅ | 좋은 [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) |
| [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) | 500 | ❌ | 깊은 비최적 경로 |

### 결론

A*, [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/), MCTS는 각각 경로 찾기, 게임 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 복잡 게임이라는 서로 다른 문제를 위해 최적화된 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 공통점은 <strong>탐색 효율성과 최적성의 트레이드오프를 어떻게 다루느냐</strong>다. A*는 [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)으로, 알파-베타는 [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)로, MCTS는 확률적 샘플링으로 각각 무한한 탐색 공간을 현실적 범위로 줄인다.

📢 **섹션 요약 비유**: A*, [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/), MCTS는 각각 영리한 탐험가, [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 체스 선수, 통계에 능한 바둑 기사다. 같은 "최선을 찾는다"는 목표이지만 전혀 다른 방법으로 접근한다.

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 경로 탐색 | A* ([A-Star](/studynote/10_ai/01_ai_basics/017_a_star_algorithm/)) | g(n)+h(n) 평가 함수, 최단 경로 |
| [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) | 맨하탄/유클리드 거리 | A* [허용적 휴리스틱](/studynote/10_ai/01_ai_basics/018_admissible_heuristic/) |
| 게임 트리 | [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/) ([Minimax](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/)) | MAX/MIN 교차 최적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) | 알파-베타 ([Alpha-Beta Pruning](/studynote/10_ai/01_ai_basics/020_alpha_beta_pruning/)) | 불필요 탐색 제거, O(b^m/2) |
| 통계 탐색 | [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) | 선택·확장·시뮬레이션·[역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/) |
| 응용 | AlphaGo | [MCTS](/studynote/10_ai/03_llm_nlp/240_mcts_monte_carlo/) + [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)/가치 네트워크 |
| 비교 | [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) | MCTS와 A*의 전신 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

### 👶 어린이를 위한 3줄 비유 설명

1. A*는 미로 찾기에서 "출구가 오른쪽이니까 오른쪽 방향으로 더 많이 탐색하자"는 눈치 있는 방법이다—무작정 모든 방향을 다 보는 것보다 훨씬 빠르다.

### 📈 관련 키워드 및 발전 흐름도

```text
완전 탐색: BFS · DFS (최적 보장 but 느림)
    |
    v
A*: g(n) + h(n) 휴리스틱 탐색 (최적 + 효율)
    |
    v
게임 AI: Minimax · α-β 가지치기 · MCTS
    |
    v
AlphaGo: MCTS + 딥러닝 정책/가치 네트워크
```
2. [미니맥스](/studynote/10_ai/03_llm_nlp/239_minimax_alpha_beta_pruning/)는 두 사람이 번갈아 두는 보드게임에서 "상대방은 나쁜 수를 두지 않는다"고 가정하고 내가 가장 유리한 수를 계산하는 방법이다.
3. MCTS는 바둑에서 "이 자리에 두면 어떻게 될까"를 수천 번 상상으로 빠르게 대국해보고 가장 많이 이긴 자리에 두는 방법이다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 236 / 258

<- **이전**: [235. AI 튜링 테스트 (Turing Test) 전문가 시스템 (Expert System) 퍼지 논리 (Fuzzy Logic)](/studynote/14_data_engineering/05_exam_keywords/235_ai_turing_test_expert_system_fuzzy_logic/)
**다음**: [237. 머신러닝 지도·비지도·강화학습 편향-분산 오류 종합](/studynote/14_data_engineering/05_exam_keywords/237_ml_supervised_unsupervised_reinforcement_bias_variance/) ->

---
