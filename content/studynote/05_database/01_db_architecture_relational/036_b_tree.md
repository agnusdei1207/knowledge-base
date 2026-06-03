+++
title = "036. B-트리 (B-Tree)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

> **핵심 인사이트**
> 1. [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) (Balanced Tree)는 모든 리프 노드가 같은 깊이에 있는 자기 균형 다진 탐색 트리로, 디스크 기반 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 표준 자료구조다 — O(log n) 검색·삽입·삭제를 보장한다.
> 2. 하나의 노드에 여러 키와 포인터를 저장해 디스크 I/O 횟수(=트리 깊이)를 최소화하며, 차수(Order) m의 [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 노드는 최대 m-1개 키와 m개 자식 포인터를 가진다.
> 3. B+Tree는 B-Tree의 변형으로 내부 노드에 포인터만 두고 리프 노드에만 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하며 리프를 링크드 리스트로 연결 — 범위 탐색(Range Scan)이 효율적이어서 RDBMS [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 표준이다.

---

## I. [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 기본 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) (차수 m=3)

```
B-Tree (Order 3, 최대 2개 키/노드):

         [30 | 70]
        /    |    \
   [10|20] [40|50] [80|90]

속성:
1. 루트: 1 <= 키 수 <= m-1
2. 내부 노드: ceil(m/2)-1 <= 키 수 <= m-1
3. 모든 리프: 동일 깊이
4. 키 정렬 유지
5. n개 키 -> n+1개 자식 포인터
```

| 차수 m | 최소 키 | 최대 키 | 최대 자식 |
|-------|--------|--------|---------|
| 3     | 1      | 2      | 3       |
| 5     | 2      | 4      | 5       |
| 51    | 25     | 50     | 51      |

> 📢 **섹션 요약 비유**: 도서관 색인 카드처럼 — 한 카드에 여러 항목을 담아 카드 수를 줄이고, 항상 균형을 유지해 찾는 시간이 일정하다.

---

## II. B+Tree vs [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">B-Tree:</div>
<div class="kb-diagram-note">내부 노드: 키 + 데이터 포인터</div>
<div class="kb-diagram-note">리프 노드: 키 + 데이터 포인터</div>
<div class="kb-diagram-tree-item" style="--depth:1">범위 탐색 시 트리 여러 경로 방문</div>
<div class="kb-diagram-note">B+Tree:</div>
<div class="kb-diagram-note">내부 노드: 키 + 자식 포인터만 (데이터 없음)</div>
<div class="kb-diagram-note">리프 노드: 키 + 데이터 포인터 + 다음 리프 링크</div>
<div class="kb-diagram-tree-item" style="--depth:1">범위 탐색: 리프 링크만 따라가면 됨</div>
</div>
</div>



| 비교       | [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)               | B+Tree              |
|-----------|----------------------|---------------------|
| 내부 노드  | 키 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)          | 키만 ([라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))        |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)     | 모든 노드            | 리프 노드만          |
| 범위 탐색  | 비효율적             | 리프 링크로 효율적   |
| 공간 효율  | 낮음                 | 높음 (내부 노드 작음)|
| 사용처     | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/))  | RDBMS [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 표준   |

> 📢 **섹션 요약 비유**: B-Tree는 책 본문에 메모를 넣은 것, B+Tree는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)만 따로 모은 책 뒤의 색인 — 범위 검색은 색인을 쭉 훑는 게 빠르다.

---

## III. 삽입과 분할 (Split)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">B+Tree (Order 3) 삽입 예시:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">10 | 20</div><div class="kb-diagram-connector">&lt;-</div><div class="kb-diagram-note">40 삽입 -&gt; 노드 가득 참</div></div>
<div class="kb-diagram-note">분할 (Split):</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">10 | 20 | 40</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">중간값 20을 부모로 올리고</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">좌:</div><div class="kb-diagram-node">10</div><div class="kb-diagram-note">우:</div><div class="kb-diagram-node">40</div></div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">20</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">10</div><div class="kb-diagram-node">40</div></div>
</div>
</div>



| 조건        | 동작          |
|------------|--------------|
| 노드 여유   | 직접 삽입     |
| 노드 가득   | Split → 부모에 중간키 올림 |
| 루트 분할   | 새 루트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)  |

> 📢 **섹션 요약 비유**: 서랍이 꽉 차면 새 서랍을 만들고 절반씩 나눠 담는 것 — 항상 균형을 유지한다.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 차수와 트리 깊이



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">블록 크기 = 4 KB = 4,096 Bytes</div>
<div class="kb-diagram-note">키 크기 = 8 Bytes (int64)</div>
<div class="kb-diagram-note">포인터 크기 = 6 Bytes</div>
<div class="kb-diagram-note">차수 m: m*8 + (m+1)*6 &lt;= 4096</div>
<div class="kb-diagram-note">14m + 6 &lt;= 4096 -&gt; m &lt;= 292</div>
<div class="kb-diagram-note">B+Tree 깊이 (10억 개 레코드):</div>
<div class="kb-diagram-note">log_292(1,000,000,000) = log(1e9)/log(292) ≈ 3.3</div>
<div class="kb-diagram-tree-item" style="--depth:0">최대 4번의 I/O로 어떤 레코드도 검색!</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 10억 개의 책 중 하나를 4번의 선반 검색으로 찾는 것 — B+Tree의 차수가 높을수록 트리가 낮고 넓어진다.

---

## V. 실무 시나리오 — PostgreSQL B+Tree [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)

```sql
-- B+Tree 인덱스 생성
CREATE INDEX idx_user_email ON users(email);

-- 범위 탐색 (B+Tree 리프 링크 활용)
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- 복합 인덱스 (Composite Index)
CREATE INDEX idx_user_status_date ON users(status, created_at);

-- 인덱스 사용 확인
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
-- Index Scan using idx_user_email -> 3-4 I/O
```

> 📢 **섹션 요약 비유**: 이메일 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 수백만 명 중에서 3번의 점프로 해당 사용자를 찾게 해주는 마법 주소록.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">B-Tree / B+Tree</div>
<div class="kb-diagram-note">+-- 속성</div>
<div class="kb-diagram-note">+-- 자기 균형 (Self-Balancing)</div>
<div class="kb-diagram-note">+-- 다진 탐색 트리 (Multi-way)</div>
<div class="kb-diagram-note">+-- O(log n) 검색·삽입·삭제</div>
<div class="kb-diagram-note">+-- B+Tree 특징</div>
<div class="kb-diagram-note">+-- 내부: 라우팅 키만</div>
<div class="kb-diagram-note">+-- 리프: 데이터 + 링크드 리스트</div>
<div class="kb-diagram-note">+-- 범위 탐색 최적</div>
<div class="kb-diagram-note">+-- 주요 연산</div>
<div class="kb-diagram-note">+-- 삽입 -&gt; Split</div>
<div class="kb-diagram-note">+-- 삭제 -&gt; Merge / 재분배</div>
<div class="kb-diagram-note">+-- 사용처</div>
<div class="kb-diagram-note">+-- RDBMS 인덱스 (PostgreSQL, MySQL InnoDB)</div>
<div class="kb-diagram-note">+-- 파일 시스템 (NTFS, HFS+, ext4)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이진 탐색 트리 (BST)</div></div>
<div class="kb-diagram-note">불균형 시 O(n) 최악</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AVL / Red-Black Tree</div></div>
<div class="kb-diagram-note">메모리 내 균형 이진 트리</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">B-Tree (Bayer &amp; McCreight, 1972)</div></div>
<div class="kb-diagram-note">디스크 최적화: 다진 트리, 노드당 다수 키</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">B+Tree</div></div>
<div class="kb-diagram-note">내부 노드 라우팅만 -&gt; 리프 링크 -&gt; 범위 탐색 최적</div>
<div class="kb-diagram-note">RDBMS 인덱스 표준</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LSM-Tree (2006~)</div></div>
<div class="kb-diagram-note">쓰기 집약 워크로드 (Cassandra, RocksDB, LevelDB)</div>
<div class="kb-diagram-note">B+Tree 대안으로 등장</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. B-트리는 도서관 책 색인처럼 한 카드에 여러 항목을 담아 빠르게 찾을 수 있게 해요.
2. 항상 균형이 잡혀 있어서, 몇 번만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 어떤 책도 찾을 수 있어요.
3. 특히 B+트리는 범위 검색에 강해서 거의 모든 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 이걸 사용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 36 / 600

← **이전**: [035. 블로킹 팩터 (Blocking Factor)](/knowledge-base/studynote/05_database/01_db_architecture_relational/035_blocking_factor/)
**다음**: [037. B+트리 (B+ Tree) — 데이터베이스 인덱스 표준](/knowledge-base/studynote/05_database/01_db_architecture_relational/037_b_plus_tree/) →

---
