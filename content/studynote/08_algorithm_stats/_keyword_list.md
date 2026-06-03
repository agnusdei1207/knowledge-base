---
title: 08. 알고리즘/자료구조/통계 키워드 목록
date: '2026-03-03'
tags:
- studynote-algorithm
---
[[267_weight_bias_activation|weight]] = 9999

# [[001_algorithm_definition|알고리즘]] / 자료구조 / 통계 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 [[001_algorithm_definition|알고리즘]]·자료구조·통계 전 영역 핵심 키워드

---

## 1. [[001_algorithm_definition|알고리즘]] 기초 — 14개

1. [[001_algorithm_definition|알고리즘]] ([[001_algorithm_definition|Algorithm]]) 정의 — 유한성/확정성/입력/출력/효율성
2. [[002_time_complexity|시간 복잡도]] ([[002_time_complexity|Time Complexity]]) — Big-O / Ω / Θ 표기법
3. [[003_space_complexity|공간 복잡도]] ([[003_space_complexity|Space Complexity]])
4. O(1) / O(log n) / O(n) / O(n log n) / O(n²) / O(2ⁿ) / O(n!)
5. [[005_divide_and_conquer|분할 정복]] ([[005_divide_and_conquer|Divide and Conquer]]) — [[014_recursion|재귀]] 분할 + 병합
6. [[006_greedy_algorithm|탐욕 알고리즘]] ([[006_greedy_algorithm|Greedy Algorithm]]) — 지역 최적 → 전체 최적
7. [[007_dynamic_programming|동적 프로그래밍]] ([[007_dynamic_programming|Dynamic Programming]]) — 최적 부분구조 + 중복 부분 문제
8. [[008_memoization|메모이제이션]] ([[008_memoization|Memoization]]) — [[402_top_down_integration|Top-Down]] DP
9. 타뷸레이션 (Tabulation) — [[403_bottom_up_integration|Bottom-Up]] DP
[[489_raid_10_hybrid|10]]. [[010_backtracking|백트래킹]] ([[010_backtracking|Backtracking]]) — [[435_pruning_hardware|가지치기]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_branch_and_bound|분기 한정]] ([[011_branch_and_bound|Branch and Bound]]) — 최적화 탐색
12. [[012_approximation_algorithm|근사 알고리즘]] ([[012_approximation_algorithm|Approximation Algorithm]]) — NP 문제
13. [[013_randomized_algorithm|랜덤화 알고리즘]] ([[013_randomized_algorithm|Randomized Algorithm]]) — Las Vegas / Monte Carlo
14. [[014_recursion|재귀]] ([[014_recursion|Recursion]]) — 기본 사례, [[014_recursion|재귀]] 사례, [[057_stack|스택]] [[095_overflow|오버플로우]]

---

## 2. 정렬 [[001_algorithm_definition|알고리즘]] — 18개

1. [[022_bubble_sort|버블 정렬]] ([[022_bubble_sort|Bubble Sort]]) — O(n²), 안정, 제자리
2. [[024_selection_sort|선택 정렬]] ([[024_selection_sort|Selection Sort]]) — O(n²), 불안정, 제자리
3. [[052_insertion_sort_algorithm|삽입 정렬]] ([[052_insertion_sort_algorithm|Insertion Sort]]) — O(n²)/O(n) 최선, 안정, 소규모 효율
4. [[029_shell_sort|셸 정렬]] ([[029_shell_sort|Shell Sort]]) — [[052_insertion_sort_algorithm|삽입 정렬]] 개선, O(n^1.5)
5. [[044_merge_sort|합병 정렬]] ([[044_merge_sort|Merge Sort]]) — O(n log n), 안정, O(n) 공간
6. [[047_quick_sort|퀵 정렬]] ([[047_quick_sort|Quick Sort]]) — 평균 O(n log n), 최악 O(n²), 불안정
7. [[015_quick_sort_optimization|퀵 정렬 최적화]] — 3-way [[514_partition_slice_volume|Partition]], Median-of-3 [[037_pivot|Pivot]]
8. [[080_heap_sort|힙 정렬]] ([[080_heap_sort|Heap Sort]]) — O(n log n), 불안정, 제자리
9. [[016_counting_sort|계수 정렬]] ([[016_counting_sort|Counting Sort]]) — O(n+k), 비교 불필요
[[489_raid_10_hybrid|10]]. [[017_radix_sort|기수 정렬]] ([[017_radix_sort|Radix Sort]]) — O(d·n), 고정 자릿수
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[018_bucket_sort|버킷 정렬]] ([[018_bucket_sort|Bucket Sort]]) — O(n) 평균, 균등 분포
12. [[019_timsort|팀 정렬]] ([[019_timsort|Timsort]]) — Python/Java 기본, 합병+삽입 혼합
13. [[020_introsort|인트로 정렬]] ([[020_introsort|Introsort]]) — 퀵+힙+삽입 혼합, C++ STL
14. [[021_stability|정렬 안정성]] ([[021_stability|Stability]]) — 동일 키 순서 유지 여부
15. [[023_external_sort|외부 정렬]] ([[023_external_sort|External Sort]]) — 대용량 [[001_dikw_pyramid|데이터]], 멀티웨이 합병
16. 정렬 비교 — 시간/공간/안정성/적합 환경
17. 네트워크 정렬 ([[027_sorting_network|Sorting Network]]) — [[430_index_fast_full_scan|병렬]] 정렬
18. [[028_binary_search|이분 탐색]] ([[031_binary_search_algorithm|Binary Search]]) — O(log n), 정렬된 [[055_array|배열]] 필수

---

## 3. 탐색 / [[070_graph_datastructure|그래프]] [[001_algorithm_definition|알고리즘]] — 24개

1. [[030_linear_search|선형 탐색]] ([[030_linear_search|Linear Search]]) — O(n)
2. [[031_binary_search_algorithm|이진 탐색]] ([[031_binary_search_algorithm|Binary Search]]) — O(log n)
3. [[032_hash_search|해시 탐색]] ([[032_hash_search|Hash Search]]) — O(1) 평균
4. [[033_graph_representation|그래프 표현]] — 인접 행렬 / 인접 리스트
5. [[034_dfs|DFS]] (Depth-First Search) — 깊이 우선, [[057_stack|스택]]/[[014_recursion|재귀]]
6. [[035_bfs|BFS]] (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
7. [[036_dijkstra|다익스트라]] ([[036_dijkstra|Dijkstra]]) — 단일 출발 최단 경로, 비음수 [[267_weight_bias_activation|가중치]]
8. [[170_bellman_ford|벨만-포드]] ([[170_bellman_ford|Bellman-Ford]]) — 음수 [[267_weight_bias_activation|가중치]] 허용, O(VE)
9. [[037_floyd_warshall|플로이드-워샬]] ([[037_floyd_warshall|Floyd-Warshall]]) — 전체 쌍 최단 경로, O(V³)
[[489_raid_10_hybrid|10]]. A* [[001_algorithm_definition|알고리즘]] — [[210_heuristics_scheduling|휴리스틱]], 최단 경로
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[039_topological_sort|위상 정렬]] ([[039_topological_sort|Topological Sort]]) — [[401_bayesian_network_dag_causality|DAG]], Kahn's / [[034_dfs|DFS]] 기반
12. [[040_scc|강연결 요소]] ([[040_scc|SCC]]) — Kosaraju / Tarjan [[001_algorithm_definition|알고리즘]]
13. [[041_mst|최소 신장 트리]] ([[041_mst|MST]]) — [[042_kruskal|Kruskal]] / Prim
14. [[042_kruskal|크루스칼]] ([[042_kruskal|Kruskal]]) — 간선 정렬 + [[070_union_find|Union-Find]]
15. 프림 (Prim) — 정점 기반, [[083_priority_queue|우선순위 큐]]
16. [[043_max_flow|최대 유량]] ([[043_max_flow|Max Flow]]) — Ford-Fulkerson / Edmonds-Karp
17. [[172_bipartite_matching|이분 매칭]] ([[172_bipartite_matching|Bipartite Matching]]) — 헝가리안 [[001_algorithm_definition|알고리즘]]
18. 유니온-파인드 ([[070_union_find|Union-Find]] / [[077_union_find_disjoint_set|Disjoint Set]]) — 경로 [[347_compaction|압축]], 랭크
19. [[045_min_cut|최소 컷]] ([[045_min_cut|Min Cut]]) — Max-Flow Min-Cut 정리
20. 오일러 경로/회로 — Fleury / Hierholzer
21. [[049_hamiltonian_path|해밀턴 경로]] — NP-완전, [[010_backtracking|백트래킹]]
22. 최소 비용 [[043_max_flow|최대 유량]] (Min-Cost Max-Flow) — 네트워크 최적화, 비용 최소화
23. 중국 우편배달 문제 (Chinese Postman Problem) — 모든 간선 순회, [[070_graph_datastructure|그래프]] 순회 최적화
24. 최장 증가 부분수열 ([[054_longest_increasing_subsequence|LIS]]) — DP / [[031_binary_search_algorithm|이진 탐색]]

---

## 4. 자료구조 — 28개

1. [[055_array|배열]] ([[055_array|Array]]) — 연속 메모리, O(1) 랜덤 접근
2. [[056_linked_list|연결 리스트]] ([[056_linked_list|Linked List]]) — 단일/이중/순환, 동적 삽입/삭제
3. [[057_stack|스택]] ([[057_stack|Stack]]) — LIFO, push/[[120_pop_point_of_production|pop]], [[014_recursion|재귀]]/[[034_dfs|DFS]]/수식 평가
4. 큐 ([[058_queue|Queue]]) — [[261_fifo_page_replacement|FIFO]], enqueue/dequeue, [[035_bfs|BFS]]/스케줄링
5. 덱 ([[084_deque|Deque]], Double-Ended [[058_queue|Queue]]) — 양방향 큐
6. [[083_priority_queue|우선순위 큐]] ([[083_priority_queue|Priority Queue]]) — 힙 기반 구현
7. 힙 ([[078_heap_datastructure|Heap]]) — 최대/최소 힙, 완전 [[060_binary_tree|이진 트리]]
8. [[060_binary_tree|이진 트리]] ([[060_binary_tree|Binary Tree]]) — 전위/중위/후위 순회
9. [[061_binary_search_tree_bst|이진 탐색 트리]] (BST) — O(log n) 평균, O(n) 최악
[[489_raid_10_hybrid|10]]. AVL 트리 — 높이 균형, 회전 (LL/[[834_load_balancing_algorithm_round_robin_least_connection|RR]]/LR/RL)
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[063_red_black_tree|레드-블랙 트리]] ([[204_red_black_tree_cfs|Red-Black Tree]]) — O(log n) 보장, Java TreeMap
12. B-트리 ([[064_b_tree|B-Tree]]) — 다진 탐색, 디스크 기반, 균형
13. B+트리 (B+Tree) — 리프 연결, DB [[154_database_index_b_tree_search_optimization|인덱스]]
14. [[087_trie|트라이]] ([[066_trie|Trie]]) — 접두사 탐색, 자동 완성
15. [[067_hash_table|해시 테이블]] ([[067_hash_table|Hash Table]]) — [[667_hash_function_integrity_one_way|해시 함수]], 충돌 처리
16. [[068_open_addressing|개방 주소법]] ([[068_open_addressing|Open Addressing]]) — 선형/이차/이중 해싱
17. [[069_chaining|체인법]] ([[103_chaining|Chaining]]) — [[056_linked_list|연결 리스트]] 충돌 처리
18. [[070_graph_datastructure|그래프]] ([[104_graph|Graph]]) — 방향/무방향, 가중/비가중
19. [[075_combinatorics|세그먼트 트리]] ([[075_combinatorics|Segment Tree]]) — 구간 [[298_qkv_attention|쿼리]]/업데이트
20. [[086_fenwick_tree|펜윅 트리]] / [[086_fenwick_tree|BIT]] (Binary [[181_indexed_addressing|Indexed]] Tree / [[106_fenwick_tree|Fenwick Tree]]) — 구간 합
21. [[073_compressed_trie|압축된 트라이]] ([[073_compressed_trie|Compressed Trie]] / Patricia [[066_trie|Trie]])
22. 서픽스 트리 (Suffix Tree) / 서픽스 [[055_array|배열]] (Suffix [[055_array|Array]])
23. 해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무
24. [[067_skip_list|스킵 리스트]] ([[110_skip_list|Skip List]]) — [[130_probability|확률]]적 균형, O(log n)
25. 유니온-파인드 ([[070_union_find|Union-Find]]) — 집합 연산
26. [[079_monotonic_stack|단조 스택]] ([[079_monotonic_stack|Monotonic Stack]]/[[058_queue|Queue]])
27. [[081_sparse_table|스파스 테이블]] ([[081_sparse_table|Sparse Table]]) — O(1) 구간 최소값 (RMQ)
28. [[061_bloomfilter|블룸 필터]] ([[061_bloomfilter|Bloom Filter]]) — [[130_probability|확률]]적 집합 멤버십, 공간 효율

---

## 5. 문자열 [[001_algorithm_definition|알고리즘]] — 12개

1. [[094_kmp_algorithm|KMP]] ([[094_kmp_algorithm|Knuth-Morris-Pratt]]) — 패턴 매칭, 실패 함수
2. [[095_boyer_moore_algorithm|보이어-무어]] ([[095_boyer_moore_algorithm|Boyer-Moore]]) — 역방향 비교, 실용적 최적
3. [[096_rabin_karp_algorithm|라빈-카프]] ([[096_rabin_karp_algorithm|Rabin-Karp]]) — 롤링 해시, 다중 패턴
4. Z [[001_algorithm_definition|알고리즘]] — 접두사 매칭 [[055_array|배열]]
5. [[098_aho_corasick|아호-코라식]] ([[098_aho_corasick|Aho-Corasick]]) — 다중 패턴 동시 매칭
6. [[099_rle|런-길이 인코딩]] ([[099_rle|RLE]]) — [[347_compaction|압축]], 연속 반복
7. [[100_huffman_coding|허프만 코딩]] ([[100_huffman_coding|Huffman Coding]]) — 가변길이 최적 코드
8. LZ77 / LZ78 / LZW — 사전 기반 [[347_compaction|압축]] (ZIP, GIF)
9. [[102_lcs_string|최장 공통 부분수열]] ([[053_lcs|LCS]]) — 문자열 비교
[[489_raid_10_hybrid|10]]. [[103_edit_distance|편집 거리]] ([[103_edit_distance|Edit Distance]], Levenshtein Distance) — DP
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[104_regex|정규 표현식]] ([[104_regex|Regex]]) — NFA/DFA, 패턴 매칭
12. 접미사 [[055_array|배열]] + [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]] — 문자열 분석

---

## 6. NP 이론 / 계산 이론 — 14개

1. P 클래스 — 다항 시간 내 해결 가능
2. NP 클래스 — 다항 시간 내 [[395_verification_process_review|검증]] 가능
3. NP-완전 ([[108_np_complete|NP-Complete]]) — NP 중 가장 어려운 문제
4. NP-어려움 ([[109_np_hard|NP-Hard]]) — NP보다 어렵거나 동등
5. P = NP 문제 — 미해결 난제
6. [[111_polynomial_reduction|다항 시간 환산]] ([[111_polynomial_reduction|Polynomial Reduction]])
7. [[103_chaining|SAT]] ([[103_chaining|Satisfiability]]) — 최초 NP-완전 증명 (Cook-Levin)
8. [[104_graph|클리크 문제]] ([[104_graph|Clique Problem]]) — NP-완전
9. 정점 커버 ([[114_vertex_cover|Vertex Cover]]) — NP-완전
[[489_raid_10_hybrid|10]]. [[106_fenwick_tree|외판원 문제]] ([[106_fenwick_tree|TSP]]) — [[109_np_hard|NP-hard]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]. 배낭 문제 ([[116_knapsack|Knapsack]] Problem) — NP-완전 (결정 [[288_version_ihl_tos_total_length|버전]])
12. [[012_approximation_algorithm|근사 알고리즘]] — ρ-근사, FPTAS, PTAS
13. 지수 시간 가설 ([[118_eth|ETH]]) — [[001_algorithm_definition|알고리즘]] 하한 도구
14. 양자 복잡도 ([[119_quantum_complexity|Quantum Complexity]]) — BQP, [[223_quantum_supremacy_advantage|양자 우위]]

---

## 7. 수치 [[001_algorithm_definition|알고리즘]] — 10개

1. 유클리드 호제법 ([[120_euclidean_algorithm|Euclidean Algorithm]]) — [[663_macos_ios_gcd_grand_central_dispatch|GCD]], O(log min)
2. [[072_sieve_of_eratosthenes|에라토스테네스의 체]] ([[072_sieve_of_eratosthenes|Sieve of Eratosthenes]]) — 소수 판별
3. 소수 판별 ([[122_primality_test|Primality Test]]) — Miller-Rabin ([[130_probability|확률]]적)
4. 거듭제곱 ([[123_fast_exponentiation|Fast Exponentiation]]) — [[005_divide_and_conquer|분할 정복]], O(log n)
5. 중국인의 나머지 정리 ([[124_crt|CRT]])
6. 가우스 소거법 ([[125_gaussian_elimination|Gaussian Elimination]]) — 연립방정식
7. [[126_fft|FFT]] (Fast Fourier Transform) — [[195_polynomial_generator_crc|다항식]] 곱, O(n log n)
8. 행렬 곱셈 ([[127_matrix_multiplication|Matrix Multiplication]]) — Strassen O(n^2.81)
9. [[128_newton_raphson|뉴턴-랩슨]] ([[128_newton_raphson|Newton-Raphson]]) — 수치 해법, 제곱근
[[489_raid_10_hybrid|10]]. [[129_monte_carlo_integration|몬테카를로 수치적분]] — [[130_probability|확률]]적 근사

---

## 8. [[130_probability|확률]] / 통계 기초 — 20개

1. [[130_probability|확률]] ([[130_probability|Probability]]) — 고전/상대도수/주관 [[130_probability|확률]]
2. 베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)
3. [[132_conditional_probability|조건부 확률]] ([[132_conditional_probability|Conditional Probability]])
4. [[133_independence|독립 사건]] ([[133_independence|Independence]]) / 상호 배타적 사건
5. [[134_random_variable|확률 변수]] ([[134_random_variable|Random Variable]]) — 이산/연속
6. [[135_expected_value|기댓값]] ([[135_expected_value|Expected Value]], E[X])
7. [[136_variance|분산]] ([[136_variance|Variance]]) / 표준편차 (Standard Deviation)
8. [[130_probability|확률]] 분포 — 이항/포아송/정규/지수/균등
9. [[138_normal_distribution|정규 분포]] ([[138_normal_distribution|Normal Distribution]]) — 68-95-99.7 규칙
[[489_raid_10_hybrid|10]]. [[139_clt|중심 극한 정리]] (Central Limit Theorem, [[139_clt|CLT]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[140_markov_chain|마르코프 체인]] ([[140_markov_chain|Markov Chain]]) — 전이 [[130_probability|확률]], 정상 분포
12. [[141_markov_property|마르코프 성질]] ([[141_markov_property|Markov Property]]) — 미래 ⊥ 과거 | 현재
13. 기대치 최대화 ([[142_em_algorithm|Expectation-Maximization]], EM [[001_algorithm_definition|알고리즘]])
14. [[143_mle|최대 우도 추정]] ([[143_mle|MLE]], Maximum Likelihood Estimation)
15. [[144_bayesian_estimation|베이즈 추정]] ([[144_bayesian_estimation|Bayesian Estimation]]) — MAP (최대 사후 [[130_probability|확률]])
16. [[145_hypothesis_testing|가설 검정]] ([[145_hypothesis_testing|Hypothesis Testing]]) — 귀무/대립 가설, [[337_p_value_significance|p-value]]
17. [[146_confidence_interval|신뢰 구간]] ([[146_confidence_interval|Confidence Interval]])
18. [[147_chi_square_test|카이제곱 검정]] ([[147_chi_square_test|Chi-Square Test]]) — 독립성 검정
19. [[070_t_test_independent_paired_mean_difference|t-검정]] / F-검정 / [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]]
20. [[149_regression_analysis|회귀 분석]] ([[149_regression_analysis|Regression Analysis]]) — 단순/다중/로지스틱

---

## 9. [[150_information_theory|정보이론]] — 10개

1. [[150_information_theory|정보이론]] ([[150_information_theory|Information Theory]]) — Shannon, 1948
2. [[151_entropy|엔트로피]] ([[151_entropy|Shannon Entropy]]) — H(X) = -Σ p·log₂p
3. [[152_mutual_information|상호 정보량]] ([[152_mutual_information|Mutual Information]])
4. KL 다이버전스 ([[153_kl_divergence|KL Divergence]]) — 분포 간 차이
5. [[154_cross_entropy|크로스 엔트로피]] ([[154_cross_entropy|Cross-Entropy]]) — [[104_classification_analysis|분류]] [[075_loss_function_cost_function|손실 함수]]
6. [[155_channel_capacity|채널 용량]] ([[155_channel_capacity|Channel Capacity]]) — 샤논 용량 공식
7. [[156_source_coding|소스 부호화 정리]] ([[156_source_coding|Source Coding Theorem]])
8. [[157_channel_coding|채널 부호화 정리]] ([[157_channel_coding|Channel Coding Theorem]]) — Shannon Limit
9. [[158_error_correcting_codes|오류 정정 부호]] (Error Correcting [[082_process_memory_structure|Code]]) — 해밍/(터보)/[[203_ldpc_low_density_parity_check|LDPC]]/폴라
[[489_raid_10_hybrid|10]]. [[347_compaction|압축]] ([[159_compression|Compression]]) — 무손실/손실, 허프만/LZ/웨이블릿

---

## [[489_raid_10_hybrid|10]]. 선형대수 / 최적화 — 10개

1. 선형 연립방정식 — 행렬 표현, 가우스 소거
2. [[161_matrix_decomposition|행렬 분해]] — LU / QR / [[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]] ([[230_svd_matrix_factorization_random_forest_xgboost_boosting|Singular Value Decomposition]])
3. 고유값 / 고유벡터 (Eigenvalue/Eigenvector)
4. [[163_pca|PCA]] ([[163_pca|Principal Component Analysis]]) — [[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]] 기반 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]
5. [[164_convex_function|볼록 함수]] ([[164_convex_function|Convex Function]]) — 전역 최적 보장
6. [[165_gradient_descent|기울기 하강법]] ([[165_gradient_descent|Gradient Descent]]) — 최적화 기본
7. [[166_lagrange_multiplier|라그랑주 승수법]] ([[166_lagrange_multiplier|Lagrange Multiplier]]) — 제약 최적화
8. [[167_linear_programming|선형 프로그래밍]] (LP) — 심플렉스법
9. [[168_integer_programming|정수 프로그래밍]] (IP) — [[011_branch_and_bound|분기 한정]], MILP
[[489_raid_10_hybrid|10]]. 진화 [[001_algorithm_definition|알고리즘]] — 유전 [[001_algorithm_definition|알고리즘]] ([[169_evolutionary_algorithms|GA]]), 입자 군집 최적화 (PSO)

---

**총 키워드 수: 160개**
