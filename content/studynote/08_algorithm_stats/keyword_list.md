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
5. [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) ([Divide and Conquer](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)) — [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 분할 + 병합
6. [탐욕 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/) ([Greedy Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/006_greedy_algorithm/)) — 지역 최적 → 전체 최적
7. [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) — 최적 부분구조 + 중복 부분 문제
8. [메모이제이션](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/) ([Memoization](/knowledge-base/studynote/08_algorithm_stats/01_basics/008_memoization/)) — [Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/) DP
9. 타뷸레이션 (Tabulation) — [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/) DP
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [백트래킹](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/) ([Backtracking](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/)) — [가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [분기 한정](/knowledge-base/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/) ([Branch and Bound](/knowledge-base/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/)) — 최적화 탐색
12. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) ([Approximation Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)) — NP 문제
13. [랜덤화 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/) ([Randomized Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/013_randomized_algorithm/)) — Las Vegas / Monte Carlo
14. [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Recursion](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) — 기본 사례, [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 사례, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [오버플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/)

---

## 2. 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 18개

1. [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/) ([Bubble Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)) — O(n²), 안정, 제자리
2. [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/) ([Selection Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)) — O(n²), 불안정, 제자리
3. [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/) ([Insertion Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)) — O(n²)/O(n) 최선, 안정, 소규모 효율
4. [셸 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/029_shell_sort/) ([Shell Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/029_shell_sort/)) — [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/) 개선, O(n^1.5)
5. [합병 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/) ([Merge Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/)) — O(n log n), 안정, O(n) 공간
6. [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/) ([Quick Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)) — 평균 O(n log n), 최악 O(n²), 불안정
7. [퀵 정렬 최적화](/knowledge-base/studynote/08_algorithm_stats/02_sorting/015_quick_sort_optimization/) — 3-way [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), Median-of-3 [Pivot](/knowledge-base/studynote/12_it_management/01_governance_strategy/037_pivot/)
8. [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/) ([Heap Sort](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)) — O(n log n), 불안정, 제자리
9. [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Counting Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) — O(n+k), 비교 불필요
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [기수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/) ([Radix Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)) — O(d·n), 고정 자릿수
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [버킷 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Bucket Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) — O(n) 평균, 균등 분포
12. [팀 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/) ([Timsort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/019_timsort/)) — Python/Java 기본, 합병+삽입 혼합
13. [인트로 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/) ([Introsort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/020_introsort/)) — 퀵+힙+삽입 혼합, C++ STL
14. [정렬 안정성](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/) ([Stability](/knowledge-base/studynote/08_algorithm_stats/02_sorting/021_stability/)) — 동일 키 순서 유지 여부
15. [외부 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/023_external_sort/) ([External Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/023_external_sort/)) — 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 멀티웨이 합병
16. 정렬 비교 — 시간/공간/안정성/적합 환경
17. 네트워크 정렬 ([Sorting Network](/knowledge-base/studynote/08_algorithm_stats/02_sorting/027_sorting_network/)) — [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 정렬
18. [이분 탐색](/knowledge-base/studynote/08_algorithm_stats/02_sorting/028_binary_search/) ([Binary Search](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)) — O(log n), 정렬된 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 필수

---

## 3. 탐색 / [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 24개

1. [선형 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/030_linear_search/) ([Linear Search](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)) — O(n)
2. [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) ([Binary Search](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)) — O(log n)
3. [해시 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/032_hash_search/) ([Hash Search](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/032_hash_search/)) — O(1) 평균
4. [그래프 표현](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/033_graph_representation/) — 인접 행렬 / 인접 리스트
5. [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) (Depth-First Search) — 깊이 우선, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)/[재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)
6. [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/) (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
7. [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) ([Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)) — 단일 출발 최단 경로, 비음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)
8. [벨만-포드](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/) ([Bellman-Ford](/knowledge-base/studynote/08_algorithm_stats/11_graph_algorithms/170_bellman_ford/)) — 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 허용, O(VE)
9. [플로이드-워샬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/) ([Floyd-Warshall](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/037_floyd_warshall/)) — 전체 쌍 최단 경로, O(V³)
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). A* [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/), 최단 경로
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [위상 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/) ([Topological Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/039_topological_sort/)) — [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/), Kahn's / [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) 기반
12. [강연결 요소](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/040_scc/) ([SCC](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/040_scc/)) — Kosaraju / Tarjan [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
13. [최소 신장 트리](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/) ([MST](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/)) — [Kruskal](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) / Prim
14. [크루스칼](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/) ([Kruskal](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/)) — 간선 정렬 + [Union-Find](/knowledge-base/studynote/12_it_management/02_itsm_itil/070_union_find/)
15. 프림 (Prim) — 정점 기반, [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)
16. [최대 유량](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/043_max_flow/) ([Max Flow](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/043_max_flow/)) — Ford-Fulkerson / Edmonds-Karp
17. [이분 매칭](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/) ([Bipartite Matching](/knowledge-base/studynote/08_algorithm_stats/12_graph_algorithms/172_bipartite_matching/)) — 헝가리안 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
18. 유니온-파인드 ([Union-Find](/knowledge-base/studynote/12_it_management/02_itsm_itil/070_union_find/) / [Disjoint Set](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/077_union_find_disjoint_set/)) — 경로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 랭크
19. [최소 컷](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/) ([Min Cut](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/045_min_cut/)) — Max-Flow Min-Cut 정리
20. 오일러 경로/회로 — Fleury / Hierholzer
21. [해밀턴 경로](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/049_hamiltonian_path/) — NP-완전, [백트래킹](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/)
22. 최소 비용 [최대 유량](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/043_max_flow/) (Min-Cost Max-Flow) — 네트워크 최적화, 비용 최소화
23. 중국 우편배달 문제 (Chinese Postman Problem) — 모든 간선 순회, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 순회 최적화
24. 최장 증가 부분수열 ([LIS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/)) — DP / [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)

---

## 4. 자료구조 — 28개

1. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) ([Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)) — 연속 메모리, O(1) 랜덤 접근
2. [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) ([Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)) — 단일/이중/순환, 동적 삽입/삭제
3. [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)) — LIFO, push/[pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/), [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)/[DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/)/수식 평가
4. 큐 ([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) — [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/), enqueue/dequeue, [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/)/스케줄링
5. 덱 ([Deque](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/), Double-Ended [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) — 양방향 큐
6. [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) ([Priority Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)) — 힙 기반 구현
7. 힙 ([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) — 최대/최소 힙, 완전 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)
8. [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/) ([Binary Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)) — 전위/중위/후위 순회
9. [이진 탐색 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/061_binary_search_tree_bst/) (BST) — O(log n) 평균, O(n) 최악
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). AVL 트리 — 높이 균형, 회전 (LL/[RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)/LR/RL)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [레드-블랙 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/) ([Red-Black Tree](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/)) — O(log n) 보장, Java TreeMap
12. B-트리 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)) — 다진 탐색, 디스크 기반, 균형
13. B+트리 (B+Tree) — 리프 연결, DB [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)
14. [트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/087_trie/) ([Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/)) — 접두사 탐색, 자동 완성
15. [해시 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) ([Hash Table](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)) — [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/), 충돌 처리
16. [개방 주소법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/068_open_addressing/) ([Open Addressing](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/068_open_addressing/)) — 선형/이차/이중 해싱
17. [체인법](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/069_chaining/) ([Chaining](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/)) — [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 충돌 처리
18. [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) — 방향/무방향, 가중/비가중
19. [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) ([Segment Tree](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)) — 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)/업데이트
20. [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) / [BIT](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) (Binary [Indexed](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) Tree / [Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)) — 구간 합
21. [압축된 트라이](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/073_compressed_trie/) ([Compressed Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/073_compressed_trie/) / Patricia [Trie](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/))
22. 서픽스 트리 (Suffix Tree) / 서픽스 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (Suffix [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))
23. 해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무
24. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/) ([Skip List](/knowledge-base/studynote/12_it_management/03_ea_isp/110_skip_list/)) — [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 균형, O(log n)
25. 유니온-파인드 ([Union-Find](/knowledge-base/studynote/12_it_management/02_itsm_itil/070_union_find/)) — 집합 연산
26. [단조 스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/) ([Monotonic Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/)/[Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))
27. [스파스 테이블](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/) ([Sparse Table](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/)) — O(1) 구간 최소값 (RMQ)
28. [블룸 필터](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/) ([Bloom Filter](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)) — [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 집합 멤버십, 공간 효율

---

## 5. 문자열 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 12개

1. [KMP](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/) ([Knuth-Morris-Pratt](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/)) — 패턴 매칭, 실패 함수
2. [보이어-무어](/knowledge-base/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/) ([Boyer-Moore](/knowledge-base/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/)) — 역방향 비교, 실용적 최적
3. [라빈-카프](/knowledge-base/studynote/08_algorithm_stats/05_string/096_rabin_karp_algorithm/) ([Rabin-Karp](/knowledge-base/studynote/08_algorithm_stats/05_string/096_rabin_karp_algorithm/)) — 롤링 해시, 다중 패턴
4. Z [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 접두사 매칭 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)
5. [아호-코라식](/knowledge-base/studynote/08_algorithm_stats/05_string/098_aho_corasick/) ([Aho-Corasick](/knowledge-base/studynote/08_algorithm_stats/05_string/098_aho_corasick/)) — 다중 패턴 동시 매칭
6. [런-길이 인코딩](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) ([RLE](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/)) — [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 연속 반복
7. [허프만 코딩](/knowledge-base/studynote/08_algorithm_stats/05_string/100_huffman_coding/) ([Huffman Coding](/knowledge-base/studynote/08_algorithm_stats/05_string/100_huffman_coding/)) — 가변길이 최적 코드
8. LZ77 / LZ78 / LZW — 사전 기반 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) (ZIP, GIF)
9. [최장 공통 부분수열](/knowledge-base/studynote/08_algorithm_stats/05_string/102_lcs_string/) ([LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)) — 문자열 비교
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/) ([Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/), Levenshtein Distance) — DP
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [정규 표현식](/knowledge-base/studynote/08_algorithm_stats/05_string/104_regex/) ([Regex](/knowledge-base/studynote/08_algorithm_stats/05_string/104_regex/)) — NFA/DFA, 패턴 매칭
12. 접미사 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) + [LCP](/knowledge-base/studynote/03_network/04_data_link_layer_error/225_lcp_link_control_protocol/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) — 문자열 분석

---

## 6. NP 이론 / 계산 이론 — 14개

1. P 클래스 — 다항 시간 내 해결 가능
2. NP 클래스 — 다항 시간 내 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능
3. NP-완전 ([NP-Complete](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/108_np_complete/)) — NP 중 가장 어려운 문제
4. NP-어려움 ([NP-Hard](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/109_np_hard/)) — NP보다 어렵거나 동등
5. P = NP 문제 — 미해결 난제
6. [다항 시간 환산](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/111_polynomial_reduction/) ([Polynomial Reduction](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/111_polynomial_reduction/))
7. [SAT](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/) ([Satisfiability](/knowledge-base/studynote/12_it_management/03_ea_isp/103_chaining/)) — 최초 NP-완전 증명 (Cook-Levin)
8. [클리크 문제](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) ([Clique Problem](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/)) — NP-완전
9. 정점 커버 ([Vertex Cover](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/114_vertex_cover/)) — NP-완전
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [외판원 문제](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) ([TSP](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)) — [NP-hard](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/109_np_hard/)
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 배낭 문제 ([Knapsack](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/116_knapsack/) Problem) — NP-완전 (결정 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))
12. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) — ρ-근사, FPTAS, PTAS
13. 지수 시간 가설 ([ETH](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/)) — [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 하한 도구
14. 양자 복잡도 ([Quantum Complexity](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/119_quantum_complexity/)) — BQP, [양자 우위](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/223_quantum_supremacy_advantage/)

---

## 7. 수치 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 10개

1. 유클리드 호제법 ([Euclidean Algorithm](/knowledge-base/studynote/08_algorithm_stats/07_numerical/120_euclidean_algorithm/)) — [GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/), O(log min)
2. [에라토스테네스의 체](/knowledge-base/studynote/12_it_management/02_itsm_itil/072_sieve_of_eratosthenes/) ([Sieve of Eratosthenes](/knowledge-base/studynote/12_it_management/02_itsm_itil/072_sieve_of_eratosthenes/)) — 소수 판별
3. 소수 판별 ([Primality Test](/knowledge-base/studynote/08_algorithm_stats/07_numerical/122_primality_test/)) — Miller-Rabin ([확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적)
4. 거듭제곱 ([Fast Exponentiation](/knowledge-base/studynote/08_algorithm_stats/07_numerical/123_fast_exponentiation/)) — [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/), O(log n)
5. 중국인의 나머지 정리 ([CRT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/124_crt/))
6. 가우스 소거법 ([Gaussian Elimination](/knowledge-base/studynote/08_algorithm_stats/07_numerical/125_gaussian_elimination/)) — 연립방정식
7. [FFT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/126_fft/) (Fast Fourier Transform) — [다항식](/knowledge-base/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) 곱, O(n log n)
8. 행렬 곱셈 ([Matrix Multiplication](/knowledge-base/studynote/08_algorithm_stats/07_numerical/127_matrix_multiplication/)) — Strassen O(n^2.81)
9. [뉴턴-랩슨](/knowledge-base/studynote/08_algorithm_stats/07_numerical/128_newton_raphson/) ([Newton-Raphson](/knowledge-base/studynote/08_algorithm_stats/07_numerical/128_newton_raphson/)) — 수치 해법, 제곱근
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [몬테카를로 수치적분](/knowledge-base/studynote/08_algorithm_stats/07_numerical/129_monte_carlo_integration/) — [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 근사

---

## 8. [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) / 통계 기초 — 20개

1. [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) ([Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) — 고전/상대도수/주관 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)
2. 베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)
3. [조건부 확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) ([Conditional Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/))
4. [독립 사건](/knowledge-base/studynote/08_algorithm_stats/08_stats/133_independence/) ([Independence](/knowledge-base/studynote/08_algorithm_stats/08_stats/133_independence/)) / 상호 배타적 사건
5. [확률 변수](/knowledge-base/studynote/08_algorithm_stats/08_stats/134_random_variable/) ([Random Variable](/knowledge-base/studynote/08_algorithm_stats/08_stats/134_random_variable/)) — 이산/연속
6. [기댓값](/knowledge-base/studynote/08_algorithm_stats/08_stats/135_expected_value/) ([Expected Value](/knowledge-base/studynote/08_algorithm_stats/08_stats/135_expected_value/), E[X])
7. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) ([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) / 표준편차 (Standard Deviation)
8. [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포 — 이항/포아송/정규/지수/균등
9. [정규 분포](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/) ([Normal Distribution](/knowledge-base/studynote/08_algorithm_stats/08_stats/138_normal_distribution/)) — 68-95-99.7 규칙
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [중심 극한 정리](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/) (Central Limit Theorem, [CLT](/knowledge-base/studynote/08_algorithm_stats/08_stats/139_clt/))
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [마르코프 체인](/knowledge-base/studynote/08_algorithm_stats/08_stats/140_markov_chain/) ([Markov Chain](/knowledge-base/studynote/08_algorithm_stats/08_stats/140_markov_chain/)) — 전이 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/), 정상 분포
12. [마르코프 성질](/knowledge-base/studynote/08_algorithm_stats/08_stats/141_markov_property/) ([Markov Property](/knowledge-base/studynote/08_algorithm_stats/08_stats/141_markov_property/)) — 미래 ⊥ 과거 | 현재
13. 기대치 최대화 ([Expectation-Maximization](/knowledge-base/studynote/08_algorithm_stats/08_stats/142_em_algorithm/), EM [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))
14. [최대 우도 추정](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/) ([MLE](/knowledge-base/studynote/08_algorithm_stats/08_stats/143_mle/), Maximum Likelihood Estimation)
15. [베이즈 추정](/knowledge-base/studynote/08_algorithm_stats/08_stats/144_bayesian_estimation/) ([Bayesian Estimation](/knowledge-base/studynote/08_algorithm_stats/08_stats/144_bayesian_estimation/)) — MAP (최대 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/))
16. [가설 검정](/knowledge-base/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/) ([Hypothesis Testing](/knowledge-base/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/)) — 귀무/대립 가설, [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/)
17. [신뢰 구간](/knowledge-base/studynote/08_algorithm_stats/08_stats/146_confidence_interval/) ([Confidence Interval](/knowledge-base/studynote/08_algorithm_stats/08_stats/146_confidence_interval/))
18. [카이제곱 검정](/knowledge-base/studynote/08_algorithm_stats/08_stats/147_chi_square_test/) ([Chi-Square Test](/knowledge-base/studynote/08_algorithm_stats/08_stats/147_chi_square_test/)) — 독립성 검정
19. [t-검정](/knowledge-base/studynote/14_data_engineering/02_math_mining/070_t_test_independent_paired_mean_difference/) / F-검정 / [ANOVA](/knowledge-base/studynote/14_data_engineering/02_math_mining/071_anova_analysis_of_variance_f_value_post_hoc/)
20. [회귀 분석](/knowledge-base/studynote/08_algorithm_stats/08_stats/149_regression_analysis/) ([Regression Analysis](/knowledge-base/studynote/08_algorithm_stats/08_stats/149_regression_analysis/)) — 단순/다중/로지스틱

---

## 9. [정보이론](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/150_information_theory/) — 10개

1. [정보이론](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/150_information_theory/) ([Information Theory](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/150_information_theory/)) — Shannon, 1948
2. [엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) ([Shannon Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/)) — H(X) = -Σ p·log₂p
3. [상호 정보량](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/) ([Mutual Information](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/))
4. KL 다이버전스 ([KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/)) — 분포 간 차이
5. [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) ([Cross-Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/)) — [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)
6. [채널 용량](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/) ([Channel Capacity](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/)) — 샤논 용량 공식
7. [소스 부호화 정리](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/156_source_coding/) ([Source Coding Theorem](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/156_source_coding/))
8. [채널 부호화 정리](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/) ([Channel Coding Theorem](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/)) — Shannon Limit
9. [오류 정정 부호](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/158_error_correcting_codes/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) — 해밍/(터보)/[LDPC](/knowledge-base/studynote/03_network/04_data_link_layer_error/203_ldpc_low_density_parity_check/)/폴라
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compression](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/)) — 무손실/손실, 허프만/LZ/웨이블릿

---

## [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 선형대수 / 최적화 — 10개

1. 선형 연립방정식 — 행렬 표현, 가우스 소거
2. [행렬 분해](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) — LU / QR / [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) ([Singular Value Decomposition](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/))
3. 고유값 / 고유벡터 (Eigenvalue/Eigenvector)
4. [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([Principal Component Analysis](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)) — [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) 기반 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)
5. [볼록 함수](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/164_convex_function/) ([Convex Function](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/164_convex_function/)) — 전역 최적 보장
6. [기울기 하강법](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/) ([Gradient Descent](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/165_gradient_descent/)) — 최적화 기본
7. [라그랑주 승수법](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/) ([Lagrange Multiplier](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/166_lagrange_multiplier/)) — 제약 최적화
8. [선형 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/167_linear_programming/) (LP) — 심플렉스법
9. [정수 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/168_integer_programming/) (IP) — [분기 한정](/knowledge-base/studynote/08_algorithm_stats/01_basics/011_branch_and_bound/), MILP
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 진화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 유전 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([GA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/169_evolutionary_algorithms/)), 입자 군집 최적화 (PSO)

---

**총 키워드 수: 160개**
