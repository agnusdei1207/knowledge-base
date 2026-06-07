---
title: "Keyword List"
date: "2026-03-03"
tags:
  - "studynote-algorithm-stats"
weight: 50
---
# [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) / 자료구조 / 통계 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)·자료구조·통계 전 영역 핵심 키워드

---

## 1. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 기초 — 14개

1. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) 정의 — 유한성/확정성/입력/출력/효율성
2. [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Time Complexity](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — Big-O / Ω / Θ 표기법
3. [공간 복잡도](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Space Complexity](/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. [O(1) / O(log n) / O(n) / O(n log n) / O(n^) / O(2ⁿ) / O(n!)](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [분할 정복](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Divide and Conquer](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — [재귀](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) 분할 + 병합
6. [탐욕 알고리즘](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Greedy Algorithm](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 지역 최적 -> 전체 최적
7. [동적 프로그래밍](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dynamic Programming](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최적 부분구조 + 중복 부분 문제
8. [메모이제이션](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Memoization](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — [Top-Down](/studynote/08_algorithm_stats/01_basics/008_memoization/) DP
9. [타뷸레이션 (Tabulation) — Bottom-Up DP](/studynote/08_algorithm_stats/01_basics/009_information_theory/)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [백트래킹](/studynote/08_algorithm_stats/01_basics/010_backtracking/) ([Backtracking](/studynote/08_algorithm_stats/01_basics/010_backtracking/)) — [가지치기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [분기 한정](/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/) ([Branch and Bound](/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/)) — 최적화 탐색
12. [근사 알고리즘](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Approximation Algorithm](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — NP 문제
13. [랜덤화 알고리즘](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([Randomized Algorithm](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — Las Vegas / Monte Carlo
14. [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Recursion](/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 기본 사례, [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 사례, [스택](/studynote/08_algorithm_stats/01_basics/014_recursion/) [오버플로우](/studynote/08_algorithm_stats/01_basics/014_recursion/)

---

## 2. 정렬 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 18개

1. [버블 정렬](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Bubble Sort](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — O(n^), 안정, 제자리
2. [선택 정렬](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Selection Sort](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — O(n^), 불안정, 제자리
3. [삽입 정렬](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Insertion Sort](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — O(n^)/O(n) 최선, 안정, 소규모 효율
4. [셸 정렬](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Shell Sort](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [삽입 정렬](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) 개선, O(n^1.5)
5. [합병 정렬](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Merge Sort](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — O(n log n), 안정, O(n) 공간
6. [퀵 정렬](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Quick Sort](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 평균 O(n log n), 최악 O(n^), 불안정
7. [퀵 정렬 최적화](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) — 3-way [Partition](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/), Median-of-3 [Pivot](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [힙 정렬](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Heap Sort](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — O(n log n), 불안정, 제자리
9. [계수 정렬](/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Counting Sort](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — O(n+k), 비교 불필요
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [기수 정렬](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Radix Sort](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — O(d·n), 고정 자릿수
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [버킷 정렬](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Bucket Sort](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — O(n) 평균, 균등 분포
12. [팀 정렬](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Timsort](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — Python/Java 기본, 합병+삽입 혼합
13. [인트로 정렬](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([Introsort](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — 퀵+힙+삽입 혼합, C++ STL
14. [정렬 안정성](/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Stability](/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 동일 키 순서 유지 여부
15. [외부 정렬](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([External Sort](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — 대용량 [데이터](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/), 멀티웨이 합병
16. [정렬 비교 — 시간/공간/안정성/적합 환경](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)
17. [네트워크 정렬 (Sorting Network) — 병렬 정렬](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)
18. [이분 탐색](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Binary Search](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — O(log n), 정렬된 [배열](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) 필수

---

## 3. 탐색 / [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 24개

1. [선형 탐색](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Linear Search](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — O(n)
2. [이진 탐색](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Binary Search](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — O(log n)
3. [해시 탐색](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Hash Search](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — O(1) 평균
4. [그래프 표현](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) — 인접 행렬 / 인접 리스트
5. [DFS](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) (Depth-First Search) — 깊이 우선, [스택](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)/[재귀](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [BFS](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
7. [다익스트라](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dijkstra](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 단일 출발 최단 경로, 비음수 [가중치](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [벨만-포드](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Bellman-Ford](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — 음수 [가중치](/studynote/08_algorithm_stats/01_basics/008_memoization/) 허용, O(VE)
9. [플로이드-워샬](/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Floyd-Warshall](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 전체 쌍 최단 경로, O(V³)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). A* [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/), 최단 경로
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [위상 정렬](/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/) ([Topological Sort](/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/)) — [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/), Kahn's / [DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) 기반
12. [강연결 요소](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([SCC](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — Kosaraju / Tarjan [알고리즘](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)
13. [최소 신장 트리](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([MST](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — [Kruskal](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) / Prim
14. [크루스칼](/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Kruskal](/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 간선 정렬 + [Union-Find](/studynote/08_algorithm_stats/01_basics/014_recursion/)
15. [프림 (Prim) — 정점 기반, 우선순위 큐](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)
16. [최대 유량](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Max Flow](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — Ford-Fulkerson / Edmonds-Karp
17. [이분 매칭](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Bipartite Matching](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — 헝가리안 [알고리즘](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)
18. [유니온-파인드 (Union-Find / Disjoint Set) — 경로 압축, 랭크](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)
19. [최소 컷](/studynote/08_algorithm_stats/02_sorting/019_timsort/) ([Min Cut](/studynote/08_algorithm_stats/02_sorting/019_timsort/)) — Max-Flow Min-Cut 정리
20. [오일러 경로/회로 — Fleury / Hierholzer](/studynote/08_algorithm_stats/02_sorting/020_introsort/)
21. [해밀턴 경로](/studynote/08_algorithm_stats/02_sorting/021_stability/) — NP-완전, [백트래킹](/studynote/08_algorithm_stats/02_sorting/021_stability/)
22. [최소 비용 최대 유량 (Min-Cost Max-Flow) — 네트워크 최적화, 비용 최소화](/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)
23. [중국 우편배달 문제 (Chinese Postman Problem) — 모든 간선 순회, 그래프 순회 최적화](/studynote/08_algorithm_stats/02_sorting/023_external_sort/)
24. [최장 증가 부분수열 (LIS) — DP / 이진 탐색](/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)

---

## 4. 자료구조 — 28개

1. [배열](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Array](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 연속 메모리, O(1) 랜덤 접근
2. [연결 리스트](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Linked List](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 단일/이중/순환, 동적 삽입/삭제
3. [스택](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Stack](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — LIFO, push/[pop](/studynote/08_algorithm_stats/01_basics/003_space_complexity/), [재귀](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)/[DFS](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)/수식 평가
4. [큐 (Queue) — FIFO, enqueue/dequeue, BFS/스케줄링](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [덱 (Deque, Double-Ended Queue) — 양방향 큐](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [우선순위 큐](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Priority Queue](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 힙 기반 구현
7. [힙 (Heap) — 최대/최소 힙, 완전 이진 트리](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)
8. [이진 트리](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Binary Tree](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — 전위/중위/후위 순회
9. [이진 탐색 트리](/studynote/08_algorithm_stats/01_basics/009_information_theory/) (BST) — O(log n) 평균, O(n) 최악
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). AVL 트리 — 높이 균형, 회전 (LL/[RR](/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)/LR/RL)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [레드-블랙 트리](/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/) ([Red-Black Tree](/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/)) — O(log n) 보장, Java TreeMap
12. [B-트리 (B-Tree) — 다진 탐색, 디스크 기반, 균형](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)
13. [B+트리 (B+Tree) — 리프 연결, DB 인덱스](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)
14. [트라이](/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Trie](/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 접두사 탐색, 자동 완성
15. [해시 테이블](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([Hash Table](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — [해시 함수](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/), 충돌 처리
16. [개방 주소법](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Open Addressing](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — 선형/이차/이중 해싱
17. [체인법](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Chaining](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — [연결 리스트](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) 충돌 처리
18. [그래프](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Graph](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — 방향/무방향, 가중/비가중
19. [세그먼트 트리](/studynote/08_algorithm_stats/02_sorting/019_timsort/) ([Segment Tree](/studynote/08_algorithm_stats/02_sorting/019_timsort/)) — 구간 [쿼리](/studynote/08_algorithm_stats/02_sorting/019_timsort/)/업데이트
20. [펜윅 트리](/studynote/08_algorithm_stats/02_sorting/020_introsort/) / [BIT](/studynote/08_algorithm_stats/02_sorting/020_introsort/) (Binary [Indexed](/studynote/08_algorithm_stats/02_sorting/020_introsort/) Tree / [Fenwick Tree](/studynote/08_algorithm_stats/02_sorting/020_introsort/)) — 구간 합
21. [압축된 트라이](/studynote/08_algorithm_stats/02_sorting/021_stability/) ([Compressed Trie](/studynote/08_algorithm_stats/02_sorting/021_stability/) / Patricia [Trie](/studynote/08_algorithm_stats/02_sorting/021_stability/))
22. [서픽스 트리 (Suffix Tree) / 서픽스 배열 (Suffix Array)](/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)
23. [해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무](/studynote/08_algorithm_stats/02_sorting/023_external_sort/)
24. [스킵 리스트](/studynote/08_algorithm_stats/02_sorting/024_selection_sort/) ([Skip List](/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)) — [확률](/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)적 균형, O(log n)
25. [유니온-파인드 (Union-Find) — 집합 연산](/studynote/08_algorithm_stats/02_sorting/025_sort_comparison/)
26. [단조 스택](/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/) ([Monotonic Stack](/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/)/[Queue](/studynote/08_algorithm_stats/02_sorting/026_insertion_sort/))
27. [스파스 테이블](/studynote/08_algorithm_stats/02_sorting/027_sorting_network/) ([Sparse Table](/studynote/08_algorithm_stats/02_sorting/027_sorting_network/)) — O(1) 구간 최소값 (RMQ)
28. [블룸 필터](/studynote/08_algorithm_stats/02_sorting/028_binary_search/) ([Bloom Filter](/studynote/08_algorithm_stats/02_sorting/028_binary_search/)) — [확률](/studynote/08_algorithm_stats/02_sorting/028_binary_search/)적 집합 멤버십, 공간 효율

---

## 5. 문자열 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 12개

1. [KMP](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Knuth-Morris-Pratt](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 패턴 매칭, 실패 함수
2. [보이어-무어](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Boyer-Moore](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 역방향 비교, 실용적 최적
3. [라빈-카프](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Rabin-Karp](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)) — 롤링 해시, 다중 패턴
4. [Z 알고리즘 — 접두사 매칭 배열](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [아호-코라식](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Aho-Corasick](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 다중 패턴 동시 매칭
6. [런-길이 인코딩](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([RLE](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — [압축](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/), 연속 반복
7. [허프만 코딩](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Huffman Coding](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 가변길이 최적 코드
8. [LZ77 / LZ78 / LZW — 사전 기반 압축 (ZIP, GIF)](/studynote/08_algorithm_stats/01_basics/008_memoization/)
9. [최장 공통 부분수열](/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([LCS](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 문자열 비교
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [편집 거리](/studynote/08_algorithm_stats/05_string/103_edit_distance/) ([Edit Distance](/studynote/08_algorithm_stats/05_string/103_edit_distance/), Levenshtein Distance) — DP
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [정규 표현식](/studynote/08_algorithm_stats/05_string/104_regex/) ([Regex](/studynote/08_algorithm_stats/05_string/104_regex/)) — NFA/DFA, 패턴 매칭
12. [접미사 배열 + LCP 배열 — 문자열 분석](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)

---

## 6. NP 이론 / 계산 이론 — 14개

1. [P 클래스 — 다항 시간 내 해결 가능](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
2. [NP 클래스 — 다항 시간 내 검증 가능](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)
3. [NP-완전 (NP-Complete) — NP 중 가장 어려운 문제](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)
4. [NP-어려움 (NP-Hard) — NP보다 어렵거나 동등](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [P = NP 문제 — 미해결 난제](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [다항 시간 환산](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Polynomial Reduction](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/))
7. [SAT](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Satisfiability](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최초 NP-완전 증명 (Cook-Levin)
8. [클리크 문제](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Clique Problem](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — NP-완전
9. [정점 커버 (Vertex Cover) — NP-완전](/studynote/08_algorithm_stats/01_basics/009_information_theory/)
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [외판원 문제](/studynote/08_algorithm_stats/06_np_theory/106_p_class/) ([TSP](/studynote/08_algorithm_stats/06_np_theory/106_p_class/)) — [NP-hard](/studynote/08_algorithm_stats/06_np_theory/109_np_hard/)
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 배낭 문제 ([Knapsack](/studynote/08_algorithm_stats/06_np_theory/116_knapsack/) Problem) — NP-완전 (결정 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))
12. [근사 알고리즘](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) — ρ-근사, FPTAS, PTAS
13. [지수 시간 가설 (ETH) — 알고리즘 하한 도구](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)
14. [양자 복잡도 (Quantum Complexity) — BQP, 양자 우위](/studynote/08_algorithm_stats/01_basics/014_recursion/)

---

## 7. 수치 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 10개

1. [유클리드 호제법 (Euclidean Algorithm) — GCD, O(log min)](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
2. [에라토스테네스의 체](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Sieve of Eratosthenes](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — 소수 판별
3. [소수 판별 (Primality Test) — Miller-Rabin (확률적)](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)
4. [거듭제곱 (Fast Exponentiation) — 분할 정복, O(log n)](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [중국인의 나머지 정리 (CRT)](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [가우스 소거법 (Gaussian Elimination) — 연립방정식](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)
7. [FFT](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) (Fast Fourier Transform) — [다항식](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) 곱, O(n log n)
8. [행렬 곱셈 (Matrix Multiplication) — Strassen O(n^2.81)](/studynote/08_algorithm_stats/01_basics/008_memoization/)
9. [뉴턴-랩슨](/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Newton-Raphson](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 수치 해법, 제곱근
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [몬테카를로 수치적분](/studynote/08_algorithm_stats/07_numerical/129_monte_carlo_integration/) — [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 근사

---

## 8. [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) / 통계 기초 — 20개

1. [확률](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Probability](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — 고전/상대도수/주관 [확률](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
2. [베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)
3. [조건부 확률](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Conditional Probability](/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. [독립 사건](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Independence](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) / 상호 배타적 사건
5. [확률 변수](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Random Variable](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 이산/연속
6. [기댓값](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Expected Value](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/), E[X])
7. [분산](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Variance](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) / 표준편차 (Standard Deviation)
8. [확률](/studynote/08_algorithm_stats/01_basics/008_memoization/) 분포 — 이항/포아송/정규/지수/균등
9. [정규 분포](/studynote/08_algorithm_stats/01_basics/009_information_theory/) ([Normal Distribution](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 68-95-99.7 규칙
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [중심 극한 정리](/studynote/08_algorithm_stats/08_stats/139_clt/) (Central Limit Theorem, [CLT](/studynote/08_algorithm_stats/08_stats/139_clt/))
[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [마르코프 체인](/studynote/08_algorithm_stats/08_stats/140_markov_chain/) ([Markov Chain](/studynote/08_algorithm_stats/08_stats/140_markov_chain/)) — 전이 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/), 정상 분포
12. [마르코프 성질](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Markov Property](/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — 미래 ⊥ 과거 | 현재
13. [기대치 최대화 (Expectation-Maximization, EM 알고리즘)](/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)
14. [최대 우도 추정](/studynote/08_algorithm_stats/01_basics/014_recursion/) ([MLE](/studynote/08_algorithm_stats/01_basics/014_recursion/), Maximum Likelihood Estimation)
15. [베이즈 추정](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) ([Bayesian Estimation](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/)) — MAP (최대 사후 [확률](/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/))
16. [가설 검정](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Hypothesis Testing](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — 귀무/대립 가설, [p-value](/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)
17. [신뢰 구간](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Confidence Interval](/studynote/08_algorithm_stats/02_sorting/017_radix_sort/))
18. [카이제곱 검정](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Chi-Square Test](/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — 독립성 검정
19. [t-검정](/studynote/08_algorithm_stats/02_sorting/019_timsort/) / F-검정 / [ANOVA](/studynote/08_algorithm_stats/02_sorting/019_timsort/)
20. [회귀 분석](/studynote/08_algorithm_stats/02_sorting/020_introsort/) ([Regression Analysis](/studynote/08_algorithm_stats/02_sorting/020_introsort/)) — 단순/다중/로지스틱

---

## 9. [정보이론](/studynote/08_algorithm_stats/09_info_theory/150_information_theory/) — 10개

1. [정보이론](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Information Theory](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) — Shannon, 1948
2. [엔트로피](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Shannon Entropy](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) — H(X) = -Σ p·log₂p
3. [상호 정보량](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) ([Mutual Information](/studynote/08_algorithm_stats/01_basics/003_space_complexity/))
4. [KL 다이버전스 (KL Divergence) — 분포 간 차이](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [크로스 엔트로피](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Cross-Entropy](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — [분류](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) [손실 함수](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
6. [채널 용량](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Channel Capacity](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 샤논 용량 공식
7. [소스 부호화 정리](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Source Coding Theorem](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/))
8. [채널 부호화 정리](/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Channel Coding Theorem](/studynote/08_algorithm_stats/01_basics/008_memoization/)) — Shannon Limit
9. [오류 정정 부호](/studynote/08_algorithm_stats/01_basics/009_information_theory/) (Error Correcting [Code](/studynote/08_algorithm_stats/01_basics/009_information_theory/)) — 해밍/(터보)/[LDPC](/studynote/08_algorithm_stats/01_basics/009_information_theory/)/폴라
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compression](/studynote/08_algorithm_stats/09_info_theory/159_compression/)) — 무손실/손실, 허프만/LZ/웨이블릿

---

## [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 선형대수 / 최적화 — 10개

1. [선형 연립방정식 — 행렬 표현, 가우스 소거](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
2. [행렬 분해](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) — LU / QR / [SVD](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Singular Value Decomposition](/studynote/08_algorithm_stats/01_basics/002_time_complexity/))
3. [고유값 / 고유벡터 (Eigenvalue/Eigenvector)](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)
4. [PCA](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) ([Principal Component Analysis](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)) — [SVD](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/) 기반 [차원 축소](/studynote/08_algorithm_stats/01_basics/004_big_o_notation/)
5. [볼록 함수](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Convex Function](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — 전역 최적 보장
6. [기울기 하강법](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Gradient Descent](/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 최적화 기본
7. [라그랑주 승수법](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Lagrange Multiplier](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 제약 최적화
8. [선형 프로그래밍](/studynote/08_algorithm_stats/01_basics/008_memoization/) (LP) — 심플렉스법
9. [정수 프로그래밍](/studynote/08_algorithm_stats/01_basics/009_information_theory/) (IP) — [분기 한정](/studynote/08_algorithm_stats/01_basics/009_information_theory/), MILP
[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 진화 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 유전 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([GA](/studynote/08_algorithm_stats/10_linear_algebra/169_evolutionary_algorithms/)), 입자 군집 최적화 (PSO)


## 추가 학습 키워드 (Additional Study Keywords)

- [n^1.5](/studynote/08_algorithm_stats/02_sorting/029_shell_sort/)
- [n](/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)
- [log n](/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)
- [Hash Search](/studynote/08_algorithm_stats/03_graph_search/032_hash_search/)
- [Graph Representation](/studynote/08_algorithm_stats/03_graph_search/033_graph_representation/)
- [Bfs](/studynote/08_algorithm_stats/03_graph_search/035_bfs/)
- [Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)
- [V³](/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)
- [A-Star Algorithm](/studynote/08_algorithm_stats/03_graph_search/038_a_star_algorithm/)
- [Scc](/studynote/08_algorithm_stats/03_graph_search/040_scc/)
- [Mst](/studynote/08_algorithm_stats/03_graph_search/041_mst/)
- [Kruskal](/studynote/08_algorithm_stats/03_graph_search/042_kruskal/)
- [Max Flow](/studynote/08_algorithm_stats/03_graph_search/043_max_flow/)
- [Merge Sort](/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/)
- [Min Cut](/studynote/08_algorithm_stats/03_graph_search/045_min_cut/)
- [Euler Path](/studynote/08_algorithm_stats/03_graph_search/046_euler_path/)
- [Quick Sort](/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)
- [Bubble Sort Algorithm](/studynote/08_algorithm_stats/03_graph_search/048_bubble_sort_algorithm/)
- [Hamiltonian Path](/studynote/08_algorithm_stats/03_graph_search/049_hamiltonian_path/)
- [Selection Sort Algorithm](/studynote/08_algorithm_stats/03_graph_search/050_selection_sort_algorithm/)
- [Tsp](/studynote/08_algorithm_stats/03_graph_search/051_tsp/)
- [Insertion Sort](/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)
- [Lcs](/studynote/08_algorithm_stats/03_graph_search/053_lcs/)
- [Longest Increasing Subsequence](/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/)
- [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/)
- [Linked List](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)
- [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/)
- [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)
- [Deque, Double-Ended Queue](/studynote/08_algorithm_stats/04_datastructure/059_deque/)
- [Binary Tree](/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)
- [Binary Search Tree, BST](/studynote/08_algorithm_stats/04_datastructure/061_binary_search_tree_bst/)
- [Adelson-Velsky and Landis Tree](/studynote/08_algorithm_stats/04_datastructure/062_avl_tree/)
- [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)
- [B+Tree](/studynote/08_algorithm_stats/04_datastructure/065_b_plus_tree/)
- [B+Tree](/studynote/08_algorithm_stats/04_datastructure/066_trie/)
- [Hash Table](/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)
- [Open Addressing](/studynote/08_algorithm_stats/04_datastructure/068_open_addressing/)
- [Chaining](/studynote/08_algorithm_stats/04_datastructure/069_chaining/)
- [Segment Tree](/studynote/08_algorithm_stats/04_datastructure/071_segment_tree/)
- [Fenwick Tree](/studynote/08_algorithm_stats/04_datastructure/072_fenwick_tree/)
- [Compressed Trie / Patricia Trie](/studynote/08_algorithm_stats/04_datastructure/073_compressed_trie/)
- [Suffix Tree Array](/studynote/08_algorithm_stats/04_datastructure/074_suffix_tree_array/)
- [Hashmap Vs Treemap](/studynote/08_algorithm_stats/04_datastructure/075_hashmap_vs_treemap/)
- [Skip List](/studynote/08_algorithm_stats/04_datastructure/076_skip_list/)
- [Union Find Disjoint Set](/studynote/08_algorithm_stats/04_datastructure/077_union_find_disjoint_set/)
- [Heap Datastructure](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)
- [Monotonic Stack](/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/)
- [Heap Sort](/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)
- [Sparse Table](/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/)
- [Bloom Filter](/studynote/08_algorithm_stats/04_datastructure/082_bloom_filter/)
- [Priority Queue](/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)
- [Deque — Double-Ended Queue](/studynote/08_algorithm_stats/04_datastructure/084_deque/)
- [Segment Tree](/studynote/08_algorithm_stats/04_datastructure/085_segment_tree/)
- [Fenwick Tree](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)
- [Trie](/studynote/08_algorithm_stats/04_datastructure/087_trie/)
- [Avl Tree](/studynote/08_algorithm_stats/04_datastructure/088_avl_tree/)
- [Rb Tree](/studynote/08_algorithm_stats/04_datastructure/089_rb_tree/)
- [B+-Tree](/studynote/08_algorithm_stats/04_datastructure/090_b_plus_tree/)
- [B-Tree](/studynote/08_algorithm_stats/04_datastructure/091_b_tree/)
- [Monotonic Queue](/studynote/08_algorithm_stats/04_datastructure/092_monotonic_stack/)
- [Skip List](/studynote/08_algorithm_stats/04_datastructure/093_skip_list/)
- [Kmp Algorithm](/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/)
- [Boyer Moore Algorithm](/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/)
- [Rabin Karp Algorithm](/studynote/08_algorithm_stats/05_string/096_rabin_karp_algorithm/)
- [Z Algorithm](/studynote/08_algorithm_stats/05_string/097_z_algorithm/)
- [Aho Corasick](/studynote/08_algorithm_stats/05_string/098_aho_corasick/)
- [Rle](/studynote/08_algorithm_stats/05_string/099_rle/)
- [Huffman Coding](/studynote/08_algorithm_stats/05_string/100_huffman_coding/)
- [Lz77 Lz78 Lzw](/studynote/08_algorithm_stats/05_string/101_lz77_lz78_lzw/)
- [Lcs String](/studynote/08_algorithm_stats/05_string/102_lcs_string/)
- [Suffix Tree & Suffix Array](/studynote/08_algorithm_stats/05_string/105_suffix_tree_array/)
- [Np Class](/studynote/08_algorithm_stats/06_np_theory/107_np_class/)
- [NP-Complete](/studynote/08_algorithm_stats/06_np_theory/108_np_complete/)
- [P Equals Np](/studynote/08_algorithm_stats/06_np_theory/110_p_equals_np/)
- [Polynomial Reduction](/studynote/08_algorithm_stats/06_np_theory/111_polynomial_reduction/)
- [Sat](/studynote/08_algorithm_stats/06_np_theory/112_sat/)
- [Clique Problem](/studynote/08_algorithm_stats/06_np_theory/113_clique_problem/)
- [Vertex Cover](/studynote/08_algorithm_stats/06_np_theory/114_vertex_cover/)
- [Tsp Np](/studynote/08_algorithm_stats/06_np_theory/115_tsp_np/)
- [Approximation Np](/studynote/08_algorithm_stats/06_np_theory/117_approximation_np/)
- [Eth](/studynote/08_algorithm_stats/06_np_theory/118_eth/)
- [Quantum Complexity](/studynote/08_algorithm_stats/06_np_theory/119_quantum_complexity/)
- [Euclidean Algorithm](/studynote/08_algorithm_stats/07_numerical/120_euclidean_algorithm/)
- [Sieve Of Eratosthenes](/studynote/08_algorithm_stats/07_numerical/121_sieve_of_eratosthenes/)
- [Primality Test](/studynote/08_algorithm_stats/07_numerical/122_primality_test/)
- [Fast Exponentiation](/studynote/08_algorithm_stats/07_numerical/123_fast_exponentiation/)
- [Crt](/studynote/08_algorithm_stats/07_numerical/124_crt/)
- [Gaussian Elimination](/studynote/08_algorithm_stats/07_numerical/125_gaussian_elimination/)
- [FFT, Fast Fourier Transform](/studynote/08_algorithm_stats/07_numerical/126_fft/)
- [Matrix Multiplication Optimization](/studynote/08_algorithm_stats/07_numerical/127_matrix_multiplication/)
- [Newton Raphson](/studynote/08_algorithm_stats/07_numerical/128_newton_raphson/)
- [Bayes Theorem](/studynote/08_algorithm_stats/08_stats/131_bayes_theorem/)
- [A|B](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)
- [Mutual Exclusivity](/studynote/08_algorithm_stats/08_stats/133_independence/)
- [Random Variable](/studynote/08_algorithm_stats/08_stats/134_random_variable/)
- [Expected Value](/studynote/08_algorithm_stats/08_stats/135_expected_value/)
- [Variance](/studynote/08_algorithm_stats/08_stats/136_variance/)
- [Probability Distributions](/studynote/08_algorithm_stats/08_stats/137_probability_distributions/)
- [Normal Distribution](/studynote/08_algorithm_stats/08_stats/138_normal_distribution/)
- [Markov Property](/studynote/08_algorithm_stats/08_stats/141_markov_property/)
- [Em Algorithm](/studynote/08_algorithm_stats/08_stats/142_em_algorithm/)
- [MLE, Maximum Likelihood Estimation](/studynote/08_algorithm_stats/08_stats/143_mle/)
- [Bayesian Estimation](/studynote/08_algorithm_stats/08_stats/144_bayesian_estimation/)
- [Hypothesis Testing](/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/)
- [Confidence Interval](/studynote/08_algorithm_stats/08_stats/146_confidence_interval/)
- [Chi Square Test](/studynote/08_algorithm_stats/08_stats/147_chi_square_test/)
- [T F Anova](/studynote/08_algorithm_stats/08_stats/148_t_f_anova/)
- [Regression Analysis](/studynote/08_algorithm_stats/08_stats/149_regression_analysis/)
- [Entropy](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)
- [Mutual Information](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/)
- [Kl Divergence](/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/)
- [Cross Entropy](/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)
- [Channel Capacity](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/)
- [Source Coding](/studynote/08_algorithm_stats/09_info_theory/156_source_coding/)
- [Channel Coding](/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/)
- [Error Correcting Codes](/studynote/08_algorithm_stats/09_info_theory/158_error_correcting_codes/)
- [Linear Equations](/studynote/08_algorithm_stats/10_linear_algebra/160_linear_equations/)
- [Matrix Decomposition](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/)
- [Eigenvalue Eigenvector](/studynote/08_algorithm_stats/10_linear_algebra/162_eigenvalue_eigenvector/)
- [Pca](/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)
- [Convex Function](/studynote/08_algorithm_stats/10_linear_algebra/164_convex_function/)
- [Gradient Descent](/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/)
- [Lagrange Multiplier](/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/)
- [Linear Programming](/studynote/08_algorithm_stats/10_linear_algebra/167_linear_programming/)
- [Integer Programming](/studynote/08_algorithm_stats/10_linear_algebra/168_integer_programming/)
- [Bellman-Ford](/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/)
- [Prim's Algorithm](/studynote/08_algorithm_stats/12_graph_algorithms/171_prim_algorithm/)
- [Bipartite Matching](/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/)
- [Merge Sort](/studynote/08_algorithm_stats/13_sorting_algorithms/173_merge_sort/)
- [Quick Sort](/studynote/08_algorithm_stats/13_sorting_algorithms/174_quick_sort/)
- [Heap Sort](/studynote/08_algorithm_stats/13_sorting_algorithms/175_heap_sort/)

---

**총 키워드 수: 160개**
