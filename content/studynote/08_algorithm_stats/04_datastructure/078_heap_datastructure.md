+++
title = "26. 힙 (Heap) — 우선순위 큐 구현의 완전 이진 트리"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 힙(Heap)은 완전 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)(Complete [Binary Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)) 형태의 자료구조로, 최대 힙(Max-Heap)에서는 부모 노드가 항상 자식보다 크고, 최소 힙(Min-Heap)에서는 부모가 항상 자식보다 작다. 이 힙 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(Heap Property)으로 인해 루트(Root)는 항상 최댓값(또는 최솟값)이 되어 O(1)에 최우선 원소를 반환한다.
> 2. **가치**: 힙은 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)([Priority Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/))의 표준 구현체로, 삽입(Push)과 삭제([Pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/)) 모두 O(log n)을 보장한다. [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) 최단 경로, 프림(Prim) [MST](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/), [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)([Heap Sort](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)), 운영체제의 프로세스 스케줄링이 모두 힙을 핵심 자료구조로 사용한다.
> 3. **판단 포인트**: 힙은 "전체 정렬"이 아닌 "부분 순서(Partial Order)" 구조다. 전체 정렬(O(n log n))이 필요하면 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 정렬이 적합하지만, "현재 최솟값만 빠르게 필요"한 경우(스트리밍 최솟값, [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))에는 힙의 O(log n) 삽입/삭제가 훨씬 효율적이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">최대 힙 구조 (배열 인덱스 기반)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">10</div><div class="kb-diagram-note">인덱스:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">/ \ 0: 10 (루트)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">8</div><div class="kb-diagram-node">9</div><div class="kb-diagram-note">1: 8</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">/ \ / \ 2: 9</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">5</div><div class="kb-diagram-node">7</div><div class="kb-diagram-node">3</div><div class="kb-diagram-node">6</div><div class="kb-diagram-note">3: 5</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4: 7 ...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">배열:</div><div class="kb-diagram-node">10, 8, 9, 5, 7, 3, 6</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">부모(i) = (i-1) // 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">왼쪽(i) = 2*i + 1, 오른쪽(i) = 2*i + 2</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 힙은 병원 응급실 대기 시스템이다. 가장 위급한 환자(최솟값/최댓값)가 항상 가장 먼저 처치받을 수 있도록, 대기 목록을 반정렬 상태로 유지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 힙 핵심 연산

```python
import heapq  # Python: 기본 최소 힙

# 힙 생성 및 사용
heap = []
heapq.heappush(heap, 5)   # O(log n)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
min_val = heapq.heappop(heap)  # O(log n): 3 반환

# heapify: 기존 리스트를 힙으로 변환 O(n)
data = [5, 3, 7, 1, 4]
heapq.heapify(data)

# 최대 힙: 값을 음수로 저장
max_heap = []
heapq.heappush(max_heap, -10)
heapq.heappush(max_heap, -5)
max_val = -heapq.heappop(max_heap)  # 10 반환
```

### Sift-Up (삽입) / Sift-Down (삭제) 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">삽입(Push): 새 원소를 마지막에 추가 → Sift-Up (부모와 비교·교환)</div>
<div class="kb-diagram-note">O(log n): 트리 높이만큼 비교</div>
<div class="kb-diagram-note">삭제(Pop): 루트를 제거 → 마지막 원소를 루트로 → Sift-Down</div>
<div class="kb-diagram-note">O(log n): 두 자식 중 더 큰/작은 값과 교환 반복</div>
</div>
</div>



- **📢 섹션 요약 비유**: Sift-Up은 신입사원이 능력에 맞는 직급(부모)을 찾아 올라가는 것이고, Sift-Down은 은퇴한 CEO 자리를 누가 채울지 아래 직급에서 선발(비교·교환)하는 것이다.

---

## Ⅲ. 비교 및 연결

| 연산 | 힙 | 정렬 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) | 비정렬 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) |
|:---|:---|:---|:---|
| **삽입** | O(log n) | O(n) | O(1) |
| **최솟값** | O(1) | O(1) | O(n) |
| **삭제 최솟값** | O(log n) | O(1) 삭제+재정렬 불필요 | O(n) |

[힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)([Heap Sort](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)):
1. 전체 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)로 힙 구성: O(n)
2. n번 [Pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/): O(n log n)
→ 총 O(n log n), 추가 공간 O(1) (In-place)

- **📢 섹션 요약 비유**: 힙과 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 정렬의 차이는 도서관 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)과 우편함 비교다. 도서관(정렬 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))은 모든 책이 정렬되어 n번째 책도 O(1)에 찾지만, 우편함(힙)은 "가장 중요한 우편"만 즉시 꺼낼 수 있고 나머지 순서는 보장 안 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서 힙 활용

```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]  # (거리, 노드) 최소 힙

    while pq:
        curr_dist, curr = heapq.heappop(pq)
        if curr_dist > dist[curr]: continue

        for next_node, weight in graph[curr]:
            new_dist = curr_dist + weight
            if new_dist < dist[next_node]:
                dist[next_node] = new_dist
                heapq.heappush(pq, (new_dist, next_node))

    return dist
# 힙 없는 다익스트라: O(V²)
# 힙 기반 다익스트라: O((V+E) log V)
```

- **📢 섹션 요약 비유**: 힙 기반 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)는 GPS 네비게이션이다. 다음에 탐색할 가장 가까운 지점을 힙에서 즉시 꺼내어(O(log n)) 불필요한 탐색 없이 최단 경로를 효율적으로 찾는다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **우선순위 처리** | 최솟값/최댓값 O(1) 접근 |
| **효율적 정렬** | [Heap Sort](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/) O(n log n) In-place |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 기반</strong> | [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/), 프림, A* 핵심 구조 |

OS 프로세스 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)([우선순위 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/180_priority_scheduling/)), [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)(Node.js, Java NIO)의 타이머 관리, 스트리밍 데이터의 상위 K개 유지([Top-K](/knowledge-base/studynote/06_ict_convergence/05_data_science/414_llm_decoder_top_k_temperature/) 문제)가 모두 힙을 핵심 자료구조로 사용한다.

- **📢 섹션 요약 비유**: 힙은 컴퓨터 세계의 VIP 대기열이다. 중요한 작업(높은 우선순위)이 들어오면 즉시 앞자리를 차지하고, 나머지는 자동으로 재정렬된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/">우선순위 큐</a></strong> | 힙의 가장 일반적인 응용 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">다익스트라</a></strong> | 힙 기반 최단 경로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/">힙 정렬</a></strong> | In-place O(n log n) 정렬 |
| <strong>완전 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/">이진 트리</a></strong> | 힙의 구조적 기반 |
| <strong>프림 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | 힙 기반 [MST](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">완전 이진 트리 — 힙의 구조적 기반</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">최소/최대 힙 — 힙 속성(Heap Property)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">우선순위 큐 — 힙의 ADT 응용</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다익스트라/프림 MST — 그래프 알고리즘 활용</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스트리밍 Top-K — 실시간 대용량 데이터 처리</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 힙은 항상 가장 중요한 것(최솟값/최댓값)이 맨 앞에 있는 특별한 줄이에요!
2. 새 사람이 들어오면 자동으로 자기 위치(우선순위 순서)를 찾아가고, 가장 앞 사람이 나가면 뒤의 사람이 자동으로 재정렬돼요.
3. OS의 작업 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)부터 네비게이션 앱까지, 우선순위가 필요한 거의 모든 곳에서 힙이 사용된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 78 / 175

← **이전**: [25. Union-Find (Disjoint Set) — 분리 집합 자료구조](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/077_union_find_disjoint_set/)
**다음**: [26. 단조 스택 (Monotonic Stack) — 다음 크거나 작은 원소 O(n) 탐색](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/) →

---
