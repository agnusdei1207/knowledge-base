+++
title = "B+트리 (B+Tree)"
date = 2026-03-05

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
- <strong>모든 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 리프 노드에만 저장</strong>하고, 리프 노드끼리 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)([Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/))로 연결하여 **순차 검색(Full Scan)** [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화한 B-트리의 변형 구조임.
- 내부 노드(Internal Node)는 경로 안내를 위한 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) 역할만 수행하여 더 많은 키를 저장할 수 있어 트리의 높이가 더욱 낮아짐.
- 현대의 관계형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(RDB) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 아키텍처에서 가장 널리 사용되는 표준 알고리즘임.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **배경:** B-트리는 순차 탐색(Range Scan) 시 트리를 중위 순회(In-order Traversal)해야 하므로 디스크 헤드 이동이 잦음. 이를 개선하기 위해 리프 노드 간 연결 구조가 필요해짐.
- **정의:** [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 세트([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) Set)와 순차 세트(Sequence Set)로 구성된 다분 균형 탐색 트리임.
- **핵심 차이:** B-트리는 모든 노드에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 담지만, B+트리는 오직 리프 노드에만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 담고 내부 노드에는 키 값만 복사하여 배치함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ B+Tree Architecture ]
         [ 20 | 40 ]           <-- Index Set (Internal Node, Pointer Only)
        /     |      \
 [10|15]   [25|30]   [45|50]   <-- Leaf Nodes (Actual Data)
   |          |          |
 [D1->D2]-->[D3->D4]-->[D5->D6] <-- Sequence Set (Linked List Connection)
```
- <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 노드(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/528_unix_inode_mechanism/">Index Node</a>):</strong> 자식 노드를 찾아가기 위한 가이드 역할만 수행. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 없음.
- **리프 노드(Leaf Node):** 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(또는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레코드 주소)가 저장되며, 다음 리프 노드를 가리키는 포인터가 있어 수평적 이동이 가능함.
- <strong>범위 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>(Range Query):</strong> 시작 키를 찾은 후 리프 노드 레벨에서 옆으로 쭉 이동하며 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽음 ($O(\log n + k)$, $k$는 범위 내 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | B-트리 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)) | B+트리 (B+Tree) |
| :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 저장</strong> | 모든 노드에 저장 | 리프 노드에만 저장 |
| **리프 연결** | 없음 (중위 순회 필요) | [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)로 연결 (순차 탐색 유리) |
| <strong>탐색 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 운 좋으면 루트에서 끝남 | 무조건 리프까지 내려가야 함 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 크기</strong> | 큼 ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포함) | 작음 (키만 포함, 더 많은 분기 가능) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **적용 사례:** MySQL InnoDB 엔진, SQL Server, IBM DB2 등 대부분의 RDBMS [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/).
- **기술사적 판단:** 특정 레코드 하나를 찾는 Point Query보다 일정 범위를 조회하는 Range Scan이 잦은 실무 환경에서는 B+트리가 절대적으로 유리함. 또한 캐시 [적중률](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/)(Cache [Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/)) 측면에서도 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 노드가 가벼운 B+트리가 유리함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 디스크 블록 접근 횟수를 최소화하면서도 범위 검색의 효율성을 극대화하여 대규모 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 시스템의 응답 속도를 보장함.
- **결론:** B+트리는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 아키텍처의 중추이며, [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소에서도 기본 원리로 확장 적용되고 있음.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) family, Multi-way Balanced Tree
- **하위/확장 개념:** [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) (Write 최적화), Fractal Tree, In-memory Indexing

### 📈 관련 키워드 및 발전 흐름도

```text
[이진 탐색 트리 (BST) — 탐색 O(log N), 불균형 시 O(N) 성능 저하]
    │
    ▼
[B-트리 (B-Tree) — 다중 분기로 디스크 I/O 최소화, 내부 노드 데이터 보유]
    │
    ▼
[B+ 트리 (B+ Tree) — 데이터 리프 집중, 리프 연결 리스트로 범위 쿼리 최적화]
    │
    ▼
[DBMS 클러스터드 인덱스 (Clustered Index) — B+ 트리 기반 물리 정렬 저장]
    │
    ▼
[LSM 트리 (Log-Structured Merge Tree) — B+ 트리 대안, 쓰기 집약 NoSQL 최적화]
```

이 흐름은 [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) 트리의 불균형 문제를 B-트리가 해결하고, B+ 트리가 범위 탐색을 최적화하여 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 표준이 된 뒤, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 집약 환경을 위한 LSM 트리로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- B-트리는 아파트 층마다 사람들이 사는 구조라면, B+트리는 1층부터 9층까지는 안내판만 있고 모든 사람은 10층에 모여 사는 구조예요.
- 10층 사람들은 옆집과 다 복도로 연결되어 있어서, 한 번 올라가면 옆집으로 바로바로 갈 수 있어요.
- 그래서 친구들 여러 명을 한꺼번에 찾을 때 훨씬 빠르고 편하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 65 / 175

← **이전**: [B-트리 (B-Tree)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)
**다음**: [B+트리 (B+Tree)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/066_trie/) →

---
