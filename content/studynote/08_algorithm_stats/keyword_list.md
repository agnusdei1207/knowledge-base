+++
title = "08. 알고리즘/자료구조/통계 키워드 목록"
date = 2026-03-03

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++
[weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) = 9999

# [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) / 자료구조 / 통계 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)·자료구조·통계 전 영역 핵심 키워드

---

## 1. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 기초 — 14개

1. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) 정의 — 유한성/확정성/입력/출력/효율성
2. [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Time Complexity](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — Big-O / Ω / Θ 표기법
3. [공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Space Complexity](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. O(1) / O(log n) / O(n) / O(n log n) / O(n²) / O(2ⁿ) / O(n!)
5. [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Divide and Conquer](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) 분할 + 병합
6. [탐욕 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Greedy Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 지역 최적 → 전체 최적
7. [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최적 부분구조 + 중복 부분 문제
8. [메모이제이션](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Memoization](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — [Top-Down](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) DP
9. 타뷸레이션 (Tabulation) — [Bottom-Up](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) DP
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [백트래킹](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/) ([Backtracking](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/)) — [가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [분기 한정](/knowledge-base/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/) ([Branch and Bound](/knowledge-base/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/)) — 최적화 탐색
12. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Approximation Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — NP 문제
13. [랜덤화 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([Randomized Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — Las Vegas / Monte Carlo
14. [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Recursion](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 기본 사례, [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 사례, [스택](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) [오버플로우](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)

---

## 2. 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 18개

1. [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Bubble Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — O(n²), 안정, 제자리
2. [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Selection Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — O(n²), 불안정, 제자리
3. [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Insertion Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — O(n²)/O(n) 최선, 안정, 소규모 효율
4. [셸 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Shell Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) 개선, O(n^1.5)
5. [합병 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Merge Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — O(n log n), 안정, O(n) 공간
6. [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Quick Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 평균 O(n log n), 최악 O(n²), 불안정
7. [퀵 정렬 최적화](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) — 3-way [Partition](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/), Median-of-3 [Pivot](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Heap Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — O(n log n), 불안정, 제자리
9. [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Counting Sort](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — O(n+k), 비교 불필요
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [기수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Radix Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — O(d·n), 고정 자릿수
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [버킷 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Bucket Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — O(n) 평균, 균등 분포
12. [팀 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Timsort](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — Python/Java 기본, 합병+삽입 혼합
13. [인트로 정렬](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([Introsort](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — 퀵+힙+삽입 혼합, C++ STL
14. [정렬 안정성](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Stability](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 동일 키 순서 유지 여부
15. [외부 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([External Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — 대용량 [데이터](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/), 멀티웨이 합병
16. 정렬 비교 — 시간/공간/안정성/적합 환경
17. 네트워크 정렬 ([Sorting Network](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — [병렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) 정렬
18. [이분 탐색](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Binary Search](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — O(log n), 정렬된 [배열](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) 필수

---

## 3. 탐색 / [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 24개

1. [선형 탐색](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Linear Search](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — O(n)
2. [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Binary Search](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — O(log n)
3. [해시 탐색](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Hash Search](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — O(1) 평균
4. [그래프 표현](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) — 인접 행렬 / 인접 리스트
5. [DFS](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) (Depth-First Search) — 깊이 우선, [스택](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)/[재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [BFS](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
7. [다익스트라](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 단일 출발 최단 경로, 비음수 [가중치](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Bellman-Ford](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — 음수 [가중치](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) 허용, O(VE)
9. [플로이드-워샬](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Floyd-Warshall](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 전체 쌍 최단 경로, O(V³)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/), 최단 경로
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [위상 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/) ([Topological Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/)) — [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/), Kahn's / [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) 기반
12. [강연결 요소](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([SCC](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — Kosaraju / Tarjan [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)
13. [최소 신장 트리](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([MST](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — [Kruskal](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) / Prim
14. [크루스칼](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Kruskal](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 간선 정렬 + [Union-Find](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)
15. 프림 (Prim) — 정점 기반, [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)
16. [최대 유량](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Max Flow](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — Ford-Fulkerson / Edmonds-Karp
17. [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Bipartite Matching](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — 헝가리안 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)
18. 유니온-파인드 ([Union-Find](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) / [Disjoint Set](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — 경로 [압축](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/), 랭크
19. [최소 컷](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/) ([Min Cut](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/)) — Max-Flow Min-Cut 정리
20. 오일러 경로/회로 — Fleury / Hierholzer
21. [해밀턴 경로](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/) — NP-완전, [백트래킹](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/)
22. 최소 비용 [최대 유량](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/) (Min-Cost Max-Flow) — 네트워크 최적화, 비용 최소화
23. 중국 우편배달 문제 (Chinese Postman Problem) — 모든 간선 순회, [그래프](/knowledge-base/studynote/08_algorithm_stats/02_sorting/023_external_sort/) 순회 최적화
24. 최장 증가 부분수열 ([LIS](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)) — DP / [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)

---

## 4. 자료구조 — 28개

1. [배열](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Array](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 연속 메모리, O(1) 랜덤 접근
2. [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Linked List](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 단일/이중/순환, 동적 삽입/삭제
3. [스택](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — LIFO, push/[pop](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/), [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)/[DFS](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)/수식 평가
4. 큐 ([Queue](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [FIFO](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/), enqueue/dequeue, [BFS](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)/스케줄링
5. 덱 ([Deque](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/), Double-Ended [Queue](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 양방향 큐
6. [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Priority Queue](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 힙 기반 구현
7. 힙 ([Heap](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최대/최소 힙, 완전 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [이진 트리](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Binary Tree](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — 전위/중위/후위 순회
9. [이진 탐색 트리](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) (BST) — O(log n) 평균, O(n) 최악
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). AVL 트리 — 높이 균형, 회전 (LL/[RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)/LR/RL)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [레드-블랙 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/) ([Red-Black Tree](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/)) — O(log n) 보장, Java TreeMap
12. B-트리 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — 다진 탐색, 디스크 기반, 균형
13. B+트리 (B+Tree) — 리프 연결, DB [인덱스](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)
14. [트라이](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Trie](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 접두사 탐색, 자동 완성
15. [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([Hash Table](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — [해시 함수](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/), 충돌 처리
16. [개방 주소법](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Open Addressing](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — 선형/이차/이중 해싱
17. [체인법](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Chaining](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) 충돌 처리
18. [그래프](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Graph](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — 방향/무방향, 가중/비가중
19. [세그먼트 트리](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/) ([Segment Tree](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/)) — 구간 [쿼리](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/)/업데이트
20. [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) / [BIT](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) (Binary [Indexed](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) Tree / [Fenwick Tree](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/)) — 구간 합
21. [압축된 트라이](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/) ([Compressed Trie](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/) / Patricia [Trie](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/))
22. 서픽스 트리 (Suffix Tree) / 서픽스 [배열](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/) (Suffix [Array](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/))
23. 해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무
24. [스킵 리스트](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/) ([Skip List](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)) — [확률](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)적 균형, O(log n)
25. 유니온-파인드 ([Union-Find](/knowledge-base/studynote/08_algorithm_stats/02_sorting/025_sort_comparison/)) — 집합 연산
26. [단조 스택](/knowledge-base/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/) ([Monotonic Stack](/knowledge-base/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/)/[Queue](/knowledge-base/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/))
27. [스파스 테이블](/knowledge-base/studynote/08_algorithm_stats/02_sorting/027_sorting_network/) ([Sparse Table](/knowledge-base/studynote/08_algorithm_stats/02_sorting/027_sorting_network/)) — O(1) 구간 최소값 (RMQ)
28. [블룸 필터](/knowledge-base/studynote/08_algorithm_stats/02_sorting/028_binary_search/) ([Bloom Filter](/knowledge-base/studynote/08_algorithm_stats/02_sorting/028_binary_search/)) — [확률](/knowledge-base/studynote/08_algorithm_stats/02_sorting/028_binary_search/)적 집합 멤버십, 공간 효율

---

## 5. 문자열 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 12개

1. [KMP](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Knuth-Morris-Pratt](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 패턴 매칭, 실패 함수
2. [보이어-무어](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Boyer-Moore](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 역방향 비교, 실용적 최적
3. [라빈-카프](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Rabin-Karp](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — 롤링 해시, 다중 패턴
4. Z [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) — 접두사 매칭 [배열](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [아호-코라식](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Aho-Corasick](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 다중 패턴 동시 매칭
6. [런-길이 인코딩](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([RLE](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — [압축](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/), 연속 반복
7. [허프만 코딩](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Huffman Coding](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 가변길이 최적 코드
8. LZ77 / LZ78 / LZW — 사전 기반 [압축](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) (ZIP, GIF)
9. [최장 공통 부분수열](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([LCS](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 문자열 비교
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/) ([Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/), Levenshtein Distance) — DP
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [정규 표현식](/knowledge-base/studynote/08_algorithm_stats/05_string/104_regex/) ([Regex](/knowledge-base/studynote/08_algorithm_stats/05_string/104_regex/)) — NFA/DFA, 패턴 매칭
12. 접미사 [배열](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) + [LCP](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) [배열](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) — 문자열 분석

---

## 6. NP 이론 / 계산 이론 — 14개

1. P 클래스 — 다항 시간 내 해결 가능
2. NP 클래스 — 다항 시간 내 [검증](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) 가능
3. NP-완전 ([NP-Complete](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — NP 중 가장 어려운 문제
4. NP-어려움 ([NP-Hard](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — NP보다 어렵거나 동등
5. P = NP 문제 — 미해결 난제
6. [다항 시간 환산](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Polynomial Reduction](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/))
7. [SAT](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Satisfiability](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최초 NP-완전 증명 (Cook-Levin)
8. [클리크 문제](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Clique Problem](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — NP-완전
9. 정점 커버 ([Vertex Cover](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — NP-완전
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [외판원 문제](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) ([TSP](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)) — [NP-hard](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/109_np_hard/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 배낭 문제 ([Knapsack](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/116_knapsack/) Problem) — NP-완전 (결정 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))
12. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) — ρ-근사, FPTAS, PTAS
13. 지수 시간 가설 ([ETH](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) 하한 도구
14. 양자 복잡도 ([Quantum Complexity](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — BQP, [양자 우위](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)

---

## 7. 수치 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 10개

1. 유클리드 호제법 ([Euclidean Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — [GCD](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), O(log min)
2. [에라토스테네스의 체](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Sieve of Eratosthenes](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 소수 판별
3. 소수 판별 ([Primality Test](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — Miller-Rabin ([확률](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)적)
4. 거듭제곱 ([Fast Exponentiation](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/), O(log n)
5. 중국인의 나머지 정리 ([CRT](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/))
6. 가우스 소거법 ([Gaussian Elimination](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 연립방정식
7. [FFT](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) (Fast Fourier Transform) — [다항식](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) 곱, O(n log n)
8. 행렬 곱셈 ([Matrix Multiplication](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — Strassen O(n^2.81)
9. [뉴턴-랩슨](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Newton-Raphson](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 수치 해법, 제곱근
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [몬테카를로 수치적분](/knowledge-base/studynote/08_algorithm_stats/07_numerical/129_monte_carlo_integration/) — [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 근사

---

## 8. [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) / 통계 기초 — 20개

1. [확률](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Probability](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 고전/상대도수/주관 [확률](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
2. 베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)
3. [조건부 확률](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Conditional Probability](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. [독립 사건](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Independence](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) / 상호 배타적 사건
5. [확률 변수](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Random Variable](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 이산/연속
6. [기댓값](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Expected Value](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/), E[X])
7. [분산](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Variance](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) / 표준편차 (Standard Deviation)
8. [확률](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) 분포 — 이항/포아송/정규/지수/균등
9. [정규 분포](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Normal Distribution](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 68-95-99.7 규칙
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [중심 극한 정리](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/) (Central Limit Theorem, [CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/))
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [마르코프 체인](/knowledge-base/studynote/08_algorithm_stats/08_stats/140_markov_chain/) ([Markov Chain](/knowledge-base/studynote/08_algorithm_stats/08_stats/140_markov_chain/)) — 전이 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/), 정상 분포
12. [마르코프 성질](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Markov Property](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — 미래 ⊥ 과거 | 현재
13. 기대치 최대화 ([Expectation-Maximization](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/), EM [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/))
14. [최대 우도 추정](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([MLE](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/), Maximum Likelihood Estimation)
15. [베이즈 추정](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([Bayesian Estimation](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — MAP (최대 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/))
16. [가설 검정](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Hypothesis Testing](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — 귀무/대립 가설, [p-value](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)
17. [신뢰 구간](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Confidence Interval](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/))
18. [카이제곱 검정](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Chi-Square Test](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — 독립성 검정
19. [t-검정](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/) / F-검정 / [ANOVA](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/)
20. [회귀 분석](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) ([Regression Analysis](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/)) — 단순/다중/로지스틱

---

## 9. [정보이론](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/150_information_theory/) — 10개

1. [정보이론](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Information Theory](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — Shannon, 1948
2. [엔트로피](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Shannon Entropy](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — H(X) = -Σ p·log₂p
3. [상호 정보량](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Mutual Information](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. KL 다이버전스 ([KL Divergence](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — 분포 간 차이
5. [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Cross-Entropy](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — [분류](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) [손실 함수](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [채널 용량](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Channel Capacity](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 샤논 용량 공식
7. [소스 부호화 정리](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Source Coding Theorem](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/))
8. [채널 부호화 정리](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Channel Coding Theorem](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — Shannon Limit
9. [오류 정정 부호](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) (Error Correcting [Code](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 해밍/(터보)/[LDPC](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/)/폴라
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compression](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/)) — 무손실/손실, 허프만/LZ/웨이블릿

---

## [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 선형대수 / 최적화 — 10개

1. 선형 연립방정식 — 행렬 표현, 가우스 소거
2. [행렬 분해](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) — LU / QR / [SVD](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Singular Value Decomposition](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/))
3. 고유값 / 고유벡터 (Eigenvalue/Eigenvector)
4. [PCA](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [SVD](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) 기반 [차원 축소](/knowledge-base/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [볼록 함수](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Convex Function](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 전역 최적 보장
6. [기울기 하강법](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 최적화 기본
7. [라그랑주 승수법](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Lagrange Multiplier](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 제약 최적화
8. [선형 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) (LP) — 심플렉스법
9. [정수 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/) (IP) — [분기 한정](/knowledge-base/studynote/08_algorithm_stats/01_basics/009_information_theory/), MILP
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 진화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 유전 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([GA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/169_evolutionary_algorithms/)), 입자 군집 최적화 (PSO)

---

**총 키워드 수: 160개**
