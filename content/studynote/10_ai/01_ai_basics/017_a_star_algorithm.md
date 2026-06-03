+++
title = "17. A* (A-Star) 알고리즘 - f(n) = g(n) + h(n), 시작점부터의 실제 비용 g(n)과 목표까지의 예상 비용 h(n)을 합산하여 최단 경로 탐색"
description = "실제 비용과 예상 비용을 합산하여 최단 경로를 탐색하는 최적 탐색 알고리즘"
date = 2024-05-24

[taxonomies]
tags = ["ai"]

[extra]
tags = ["ai"]
+++

# 17. A* (A-Star) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 현재까지의 실제 이동 비용 \(g(n)\)과 목표까지의 예상 비용 \(h(n)\)을 합산한 평가 함수 \(f(n)\)을 기준으로, 가장 유망한 노드를 우선 탐색하는 지향성(Informed) [그래프 탐색](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/613_graph_bfs_memory/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))의 완벽성과 그리디 탐색(Greedy [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/))의 속도를 결합하여, [허용적 휴리스틱](/knowledge-base/studynote/10_ai/01_ai_basics/018_admissible_heuristic/) 조건 하에서 최적 경로(최단 거리)를 완벽하게 보장한다.
> 3. **융합**: 자율주행 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 게임 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 길찾기(Pathfinding), 로보틱스 모션 플래닝 등에서 공간 탐색 폭발을 막아주는 핵심 인프라로 쓰인다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

과거 시스템에서 목적지까지의 최단 경로를 찾기 위해 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이나 [너비 우선 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/)([BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/))을 사용했다. 그러나 이들은 목표의 방향을 전혀 모른 채 물결치듯 모든 방향으로 탐색을 확장([Uninformed Search](/knowledge-base/studynote/10_ai/01_ai_basics/014_uninformed_search/))하므로, 공간과 연산 리소스를 기하급수적으로 낭비했다. 이를 해결하기 위해 목표까지 남은 거리에 대한 '직관([Heuristic](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/236_a_star_heuristic_minimax_mcts_monte_carlo/))'을 도입하여 탐색에 뚜렷한 방향성을 제시한 것이 A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 

이 도식은 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)(맹목적)와 A*([휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 적용)의 탐색 공간 차이를 보여주는 비교 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)이다. S는 출발지, G는 목적지를 뜻한다.

```text
[Dijkstra 다익스트라의 탐색 범위]      [A* 알고리즘의 탐색 범위]
       (동심원 형태 확장)                (타원형 지향성 확장)
        ___-------___                     
    _---             ---_                  __---_
  _-         (G)         -_              _-      _ (G)
 -             |           -            /     __-
|       ___----|----___     |          |  _--
|   _---       |       ---_ |          | /  
 -_-          (S)          -_-          (S)
   -                     -                 
    ---___         ___---               
          ---------
```

이 비교 그림의 핵심은 탐색 공간(원과 타원의 면적)의 크기 차이다. [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)는 S에서 G의 반대 방향으로도 무의미한 탐색을 강행하는 반면, A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 목적지 G 방향으로 탐색 빔을 집중시켜 불필요한 노드 방문을 극적으로 잘라낸다. 따라서 대규모 지도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등에서 A*는 시스템 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 높이고 메모리 고갈을 방지하는 결정적 이점을 제공한다.

> 📢 **섹션 요약 비유**: 서울에서 부산으로 갈 때, 나침반 없이 무작정 전국 모든 도로를 다 달려보고 고르는 것이 아니라, 남쪽이라는 '방향 감각([휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/))'을 추가해 남쪽 도로만 우선적으로 탐색하는 내비게이션과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 판단 기준이 되는 핵심 평가 함수는 다음과 같다.
**\(f(n) = g(n) + h(n)\)**

| 파라미터 | 명칭 | 내부 동작 및 의미 |
|:---|:---|:---|
| **\(f(n)\)** | 평가 함수 (Evaluation Func) | 노드 n을 거쳐가는 경로의 총 예상 비용. 이 값이 가장 작은 노드가 다음 탐색 대상. |
| **\(g(n)\)** | 실제 비용 (Path Cost) | 시작점(Start)에서 현재 노드 n까지 도달하는 데 실제로 지불한 누적 확정 비용. |
| **\(h(n)\)** | [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) ([Heuristic](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/236_a_star_heuristic_minimax_mcts_monte_carlo/) Cost) | 현재 노드 n에서 목표(Goal)까지 남은 '예상' 비용. ([유클리디안 거리](/knowledge-base/studynote/05_database/06_dw_olap_trends/350_ann/), 맨해튼 거리 등) |

[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 내부적으로 **Open List(탐색 대기열)** 와 **Closed List(방문 완료열)** 라는 두 개의 큐 구조를 운영하여 상태를 전이시킨다. 



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">A* 상태 전이 메커니즘</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">1.</div><div class="kb-diagram-node">Start</div><div class="kb-diagram-note">노드를 Open List에 삽입</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">2. Open List에서 f(n)이 가장 작은 노드</div><div class="kb-diagram-node">X</div><div class="kb-diagram-note">추출 │◄──</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">3.</div><div class="kb-diagram-node">X</div><div class="kb-diagram-note">가 목표(Goal)인가? │</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─</div><div class="kb-diagram-node">YES</div><div class="kb-diagram-note">──► 탐색 종료 (경로 반환) │</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─</div><div class="kb-diagram-node">NO</div><div class="kb-diagram-note">──►</div><div class="kb-diagram-node">X</div><div class="kb-diagram-note">를 Closed List로 이동 │</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">4.</div><div class="kb-diagram-node">X</div><div class="kb-diagram-note">의 이웃 노드 전개 │</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(이미 Closed에 있다면 무시)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(g(n) + h(n)을 계산하여 이웃 노드의 f(n) 갱신)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Open List에 정렬 삽입 혹은 더 적은 g로 갱신)</div></div>
</div>
</div>



이 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 흐름도의 병목 지점은 'Open List에서 가장 작은 f(n)을 찾는 과정'이다. 노드 수가 수백만 개로 늘어나면 이 리스트를 정렬하고 갱신하는 연산이 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지배한다. 따라서 실무에서는 Open List를 단순 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 아닌 최소 힙(Min-[Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))이나 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)([Priority Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)) 기반으로 구현하여 접근 복잡도를 O(log N)으로 방어해야 한다.

> 📢 **섹션 요약 비유**: 부동산을 살 때, "지금까지 낸 계약금(g)"에다가 "앞으로 내야 할 잔금(h)"을 합쳐서, "총 견적(f)"이 가장 저렴한 집부터 순서대로 방문하며 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 과정과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

A* 탐색은 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 함수 \(h(n)\)의 비중에 따라 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 본질 자체가 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)나 그리디 탐색으로 완전히 변신하는 유연성을 가진다.

| 조건 판단 | 사용 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 전환 | 비용 계산식 | 경로 최적성 | 탐색 속도 |
|:---|:---|:---|:---:|:---:|
| **\(h(n) = 0\)** | [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) | \(f(n) = g(n)\) | 절대적 보장 | 매우 느림 |
| **\(h(n) \le h^*(n)\)** | **A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)** | \(f(n) = g(n) + h(n)\) | 절대적 보장 | 빠름 |
| **\(g(n) = 0\)** | 그리디 탐색 (Greedy [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/)) | \(f(n) = h(n)\) | 보장 실패 | 극도로 빠름 |

이 매트릭스는 A*가 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)와 그리디 탐색을 양극단으로 하는 스펙트럼의 중앙에 위치함을 보여준다. \(h(n)\)이 0이 되면 목적지 방향 감각을 완전히 상실하여 무지성 탐색([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))이 되고, 반대로 지금까지 온 거리 \(g(n)\)을 무시하고 오직 목표 방향 \(h(n)\)만 쫓게 되면 최단 거리를 무시한 채 벽에 부딪히는 맹목적 추격(Greedy)이 된다. A*는 이 둘의 완벽한 밸런스를 잡아주는 수학적 구조를 갖는다.

> 📢 **섹션 요약 비유**: A*는 과거의 노력(g)과 미래의 희망(h)을 정확히 5:5로 합산하여 결정하는 지혜로운 투자자이고, 다른 방법들은 하나만 극단적으로 맹신하는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무 환경(예: 모바일 게임 서버, 실시간 로봇 제어)에서 A*를 무턱대고 돌리면 메모리 초과([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/), [Out Of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 장애가 발생한다. A*는 지나온 모든 노드를 기억해야 하므로 [공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)가 O(b^d)로 기하급수적이기 때문이다.

<strong>도입 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a> 및 실무 방어 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>
- **메모리 병목 방어**: 거대한 지도에서는 전체 A* 대신 메모리 제한적 A*인 **SMA* (Simplified Memory-Bounded A*)<strong> 나 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/">분할 정복</a> 방식인 </strong>[HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)* (Hierarchical Pathfinding A*)** 를 도입해야 한다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/">휴리스틱</a>(h) 선택</strong>: 타일 맵의 대각선 이동 허용 여부에 따라 맨해튼 거리(수직/수평만 허용)와 체비셰프 거리(대각선 허용)를 다르게 채택해야 연산 효율이 극대화된다.

```text
[실무 안티패턴 시각화: 휴리스틱 과대평가(Overestimation) 함정]

  (S) ---(비용 5)--- (A) ---(비용 5)--- (G)   [실제경로비용: 10]
   |
   +-----(비용 15)----------------------+ (G)

* 만약 h(A) = 20 으로 너무 크게 예상해버린다면?
  f(A) = 5 + 20 = 25.
  반면 밑의 우회 경로 f(밑) = 15 + 0 = 15.
  => 알고리즘은 최단경로(위쪽)를 버리고 비용이 15인 멍청한 우회 경로를 최적이라고 확정해버림.
```

이 장애 전파도는 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 디자인이 잘못되었을 때 시스템이 어떻게 최적해를 누락하는지 정확히 보여준다. \(h(n)\)은 반드시 실제 남은 거리보다 작거나 같아야(Admissible) 최적해를 보장한다. 이 조건을 어기는 순간 A*는 길찾기 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 완전히 상실한다.

> 📢 **섹션 요약 비유**: 예상 비용(견적)을 실제보다 너무 부풀려 잡으면, 더 좋은 지름길을 애초에 포기해버리고 바가지요금 경로를 선택하는 악성 계약을 맺는 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 1968년 제안된 이래 탐색 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)의 불변하는 표준 규격으로 자리매김했다. [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)이라는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식을 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 내부로 주입함으로써 연산 복잡도를 기계 수준이 아닌 인간의 직관 수준으로 낮출 수 있음을 증명했다.

미래의 길찾기 시스템은 A*를 딥러닝과 결합하여 진화하고 있다. 즉, 전통적인 맨해튼 거리 수식을 쓰는 대신, 복잡한 실시간 교통 체증 상황을 [Graph Neural Network](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/) ([GNN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/159_gnn_graph_neural_network_message_passing/))가 학습하여 최적의 동적 \(h(n)\) 값을 실시간으로 추론해 A*에 주입하는 하이브리드 신경망 탐색이 차세대 자율주행 표준으로 연구되고 있다.

> 📢 **섹션 요약 비유**: 고전적인 지도책([다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))에, 실시간 교통 상황을 알려주는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 두뇌([휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/))를 장착하여 완벽한 길을 찾아내는 최강의 콤비 플레이와 같습니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">다익스트라</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">Dijkstra</a>)</strong> | A*에서 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 요소가 배제된 가장 기본적인 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 최단 경로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/018_admissible_heuristic/">허용적 휴리스틱</a> (<a href="/knowledge-base/studynote/10_ai/01_ai_basics/018_admissible_heuristic/">Admissible Heuristic</a>)</strong> | A*가 반드시 가장 빠른 최적 경로를 찾아내기 위한 수학적 필수 보장 조건
- **맨해튼 거리 (Manhattan Distance)** | 격자형(Grid) 지도상에서 X축과 Y축 차이의 절대값을 합산한 대표적 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 함수
- <strong>그리디 맹목 탐색 (Greedy <a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/">BFS</a>)</strong> | 현재까지 온 거리는 무시하고 오직 목표 깃발만 보고 달리는 맹목적 돌격 탐색기
- **Open List / Closed List** | A*의 상태를 저장하는 방문 [대기 큐](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/) 구조와 이미 확정된 [캐시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/259_cache_memory/)

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">BFS (너비 우선 탐색) — 최단 홉 탐색, 가중치 무시, 메모리 폭발</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다익스트라 (Dijkstra) — 가중치 최단 경로, g(n) 기반, 목표 방향성 없음</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">A* 알고리즘 — f(n) = g(n) + h(n), 휴리스틱으로 탐색 공간 대폭 축소</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">IDA* (Iterative Deepening A*) — 메모리 O(d), 깊이 제한 반복 심화 탐색</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">JPS (Jump Point Search) — 균일 격자에서 A* 불필요 노드 건너뜀, 수십 배 속도</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">신경망 휴리스틱 (Neural Heuristic) — 학습된 h(n)으로 복잡 환경 경로 계획</div></div>
</div>
</div>


이 흐름은 방향성 없는 BFS에서 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)를 거쳐 목표 지향 A*로 수렴하고, 메모리·속도 최적화와 학습 기반 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)으로 진화하는 경로 탐색 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 미로 속에서 보물을 찾을 때, 왔던 길을 다 외우고 다니는 건 너무 머리 아프고 힘들죠.
2. A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 "지금까지 걸어온 걸음 수(g)"와 "보물까지 대충 남은 거리(h)"를 머릿속으로 합쳐봐요.
3. 그리고 그 합친 숫자가 가장 작은, 즉 제일 똑똑하고 빠른 길부터 골라서 전진하는 똑똑한 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)가랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 17 / 420

← **이전**: [16. 언덕 오르기 탐색 (Hill Climbing) - 현재 상태에서 이웃 상태 중 가장 좋은 곳으로만 이동 (지역 최적해에 빠질 위험)](/knowledge-base/studynote/10_ai/01_ai_basics/016_hill_climbing/)
**다음**: [18. 허용적 휴리스틱 (Admissible Heuristic) - A*가 최적해를 보장하기 위한 조건, h(n)이 실제 목표까지의 비용을](/knowledge-base/studynote/10_ai/01_ai_basics/018_admissible_heuristic/) →

---
