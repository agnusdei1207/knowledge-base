+++
title = "27. 힙 정렬 (Heap Sort) — 힙 자료구조 기반 비교 정렬"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 힙 정렬([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) Sort)은 최대 힙(Max-[Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))을 이용하여 배열을 정렬하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, Heapify(힙 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) -> Extract-Max(루트 추출) 반복의 2단계로 O(n log n) [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)와 O(1) 추가 공간을 달성하는 제자리(In-place) 비교 정렬이다.
> 2. **가치**: 힙 정렬의 핵심 가치는 최악·평균·최선 모두 O(n log n)을 보장하는 유일한 제자리 정렬이라는 점이다. [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)은 최악 O(n^), 병합 정렬은 O(n) 추가 공간이 필요하다. 따라서 메모리 제약 + 최악 케이스 보장이 요구되는 환경에 적합하다.
> 3. **판단 포인트**: 실무에서 힙 정렬은 캐시 지역성(Cache Locality)이 낮아 [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)보다 느린 경우가 많다. 힙의 임의 접근 패턴(Random Access)이 CPU 캐시 미스를 유발하기 때문이다. 이런 이유로 실제 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 정렬(Python [TimSort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/), Java Dual-Pivot QuickSort)에서는 힙 정렬을 단독으로 거의 사용하지 않는다.

---

## Ⅰ. 개요 및 필요성

```text
힙 정렬 2단계:

1단계: Build Max-Heap (O(n))
  [3,1,6,5,2,4] -> 힙화 -> [6,5,4,3,2,1]
                                (최대 힙)

2단계: Extract-Max 반복 (n-1번, 각 O(log n))
  [6,5,4,3,2,1] -> 6 추출·말단 교환 -> Heapify
  -> [5,3,4,1,2|6] -> 5 추출... 반복
  -> 정렬 완료: [1,2,3,4,5,6]
```

- **📢 섹션 요약 비유**: 힙 정렬은 사장을 반복 해고하는 인사 시스템이다. 회사(힙)에서 가장 능력 있는 사람(최대값)을 계속 뽑아 정렬된 명단에 추가하고, 남은 직원 중 새로운 사장을 선출하는 과정을 반복한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Heapify (하향식 힙 복원)

```text
Max-Heap 속성: parent ≥ children

Heapify(i):
  left  = 2i+1
  right = 2i+2
  largest = max(arr[i], arr[left], arr[right])
  if largest != i:
      swap(arr[i], arr[largest])
      Heapify(largest)  // 재귀

시간 복잡도: O(log n)
```

### 전체 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)

| 단계 | 복잡도 |
|:---|:---|
| Build [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) | O(n) |
| n-1번 Extract-Max | O(n log n) |
| **전체** | **O(n log n)** |
| [공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) | O(1) 제자리 |

- **📢 섹션 요약 비유**: Heapify는 새 사장 선출 과정이다. 빈 사장 자리(루트)에 말단 직원이 올라오면, 더 능력 있는 부하와 계속 자리를 바꾸면서 적절한 위치를 찾아 내려간다.

---

## Ⅲ. 비교 및 연결

| 비교 | 힙 정렬 | [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/) | 병합 정렬 |
|:---|:---|:---|:---|
| 최악 시간 | O(n log n) | O(n^) | O(n log n) |
| 평균 시간 | O(n log n) | O(n log n) | O(n log n) |
| 공간 | O(1) | O(log n) | O(n) |
| 캐시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 낮음 | 높음 | 중간 |
| 안정 정렬 | 아니오 | 아니오 | 예 |

- **📢 섹션 요약 비유**: 힙 정렬은 법적으로 완벽한 판사(최악 보장)지만 처리 속도가 느리다. [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)은 빠른 판사지만 가끔 최악의 날이 있다. 병합 정렬은 빠르고 공정하지만 사무실(메모리)이 두 배 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 힙 정렬의 실제 사용처
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/">우선순위 큐</a> 구현</strong>: 힙 정렬의 핵심 자료구조인 힙이 직접 활용.
- **K번째 최댓값 탐색**: 힙을 이용해 O(n + k log n)으로 효율적 해결.
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/">IntroSort</a></strong>: C++ STL std::sort. [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)이 깊어지면 힙 정렬로 전환 -> O(n log n) 최악 보장.

### [IntroSort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) (하이브리드)
```text
IntroSort = QuickSort + HeapSort + InsertionSort
- 재귀 깊이 < 2log n: QuickSort
- 재귀 깊이 ≥ 2log n: HeapSort (최악 방지)
- 파티션 크기 ≤ 16: InsertionSort (소규모 최적)
```

- **📢 섹션 요약 비유**: IntroSort는 상황별 최적 요리사 팀이다. 일반적으로 빠른 셰프(QuickSort)가 요리하다가 복잡해지면 안정적인 셰프(HeapSort)가 교대하고, 소규모 주문엔 빠른 서빙 직원(InsertionSort)이 담당한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **최악 보장** | O(n log n) 최악 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) |
| **제자리 정렬** | O(1) 추가 공간 |
| **임베디드 활용** | 메모리 제약 환경에서 안정적 정렬 |

힙 정렬은 단독 정렬보다 [IntroSort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/)·PDQSort 같은 하이브리드 정렬의 안전망 역할로 발전했으며, [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)·[스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)·[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/), 프림)의 핵심 자료구조로 더 넓게 활용된다.

- **📢 섹션 요약 비유**: 힙은 회사에서 항상 가장 중요한 업무(우선순위)를 맨 위에 올려두는 작업 큐다. 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)보다 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)로서의 역할이 현대 컴퓨팅에서 더 중요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Max-<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">Heap</a></strong> | 힙 정렬의 핵심 자료구조 |
| **Heapify** | 힙 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 복원 핵심 연산 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/">우선순위 큐</a></strong> | 힙의 주요 응용 자료구조 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/">IntroSort</a></strong> | 힙 정렬 + [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/) 하이브리드 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">다익스트라</a></strong> | 최소 힙 기반 최단 경로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[선택 정렬 — O(n^) 기본 선택 기반 정렬]
    |
    v
[힙 자료구조 — O(log n) 최대·최소값 추출]
    |
    v
[힙 정렬 — O(n log n) 제자리 정렬]
    |
    v
[IntroSort — 힙+퀵+삽입 하이브리드 최적화]
    |
    v
[우선순위 큐 응용 — 스케줄러, 다익스트라, A*]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 힙 정렬은 반장 선출 반복 게임이에요! 가장 키 큰 사람(최댓값)을 뽑아 줄 세우고, 남은 중에서 또 반장 선출, 반복!
2. 어떤 경우에도 O(n log n) 시간이 보장되는 안정적인 방법이에요 - 다만 CPU 캐시를 잘 활용하지 못해서 [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)보다 느릴 때도 있어요.
3. 현대 컴퓨터에서는 힙 정렬보다 힙 자료구조 자체가 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)·길 찾기 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 더 많이 쓰인답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 80 / 175

<- **이전**: [26. 단조 스택 (Monotonic Stack) — 다음 크거나 작은 원소 O(n) 탐색](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/)
**다음**: [27. 스파스 테이블 (Sparse Table) — 정적 RMQ 최적 자료구조](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/) ->

---
