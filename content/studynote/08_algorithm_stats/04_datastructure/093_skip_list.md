+++
title = "스킵 리스트 (Skip List)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

> **핵심 인사이트 3줄**
> 1. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)([Skip List](/knowledge-base/studynote/12_it_management/03_ea_isp/894_skip_list/))는 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 다중 레벨 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)로, 균형 [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) 트리와 동일한 O(log n) 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 단순한 구조로 달성하는 자료구조다.
> 2. 각 노드가 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) p(=0.5)로 상위 레벨에 복사되어 "고속도로 레이어"를 형성하며, 이 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 균형이 결정적 균형 트리(AVL·RB)의 복잡한 회전 연산을 대체한다.
> 3. Redis의 Sorted Set(zset), LevelDB의 [MemTable](/knowledge-base/studynote/05_database/07_exam_summary/494_memtable_sstable_flush/), MemSQL 등에서 실제로 사용되며, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리·락프리([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) 구현에 유리해 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조로 주목받는다.

---

## Ⅰ. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)의 구조와 개념

[스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)([Skip List](/knowledge-base/studynote/12_it_management/03_ea_isp/894_skip_list/))는 <strong>William Pugh(1990)</strong>가 제안한 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 자료구조다.

```
레벨 3: HEAD ------------------------ 25 ------------ NULL
레벨 2: HEAD -------- 10 ------------ 25 ---- 40 ----- NULL
레벨 1: HEAD -- 5 -- 10 -- 15 ------ 25 -- 35 -- 40 -- NULL
레벨 0: HEAD -- 5 -- 10 -- 15 -- 20 -- 25 -- 30 -- 35 -- 40 -- NULL
            (기본 연결 리스트)
```

### 핵심 특성

- **레벨 0**: 모든 요소를 포함한 완전 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)
- **상위 레벨**: [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 선택된 요소만 포함 (빠른 건너뛰기)
- **노드 높이**: 동전 던지기(p=0.5)로 결정
- **예상 높이**: O(log n)

📢 **섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)는 서울 지하철 시스템이다 — 일반 역(레벨 0), 환승역(레벨 1), 급행 정차역(레벨 2)처럼 중요도에 따라 여러 층의 노선이 있어 목적지까지 빠르게 이동한다.

---

## Ⅱ. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/) 탐색 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

```python
def search(skip_list, target):
    current = skip_list.head
    # 최상위 레벨부터 시작
    for level in range(skip_list.max_level - 1, -1, -1):
        # 현재 레벨에서 target 이상이 나올 때까지 전진
        while (current.forward[level] is not None and
               current.forward[level].val < target):
            current = current.forward[level]
    # 레벨 0으로 내려와 실제 값 확인
    current = current.forward[0]
    if current and current.val == target:
        return current
    return None
```

### 탐색 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)

```
15를 검색:
레벨 3: HEAD -> (25 초과 -> 하강)
레벨 2: HEAD -> 10 -> (25 초과 -> 하강)
레벨 1: HEAD -> 10 -> 15 발견 -> 레벨 0 확인 -> ✓
비교 횟수: 4회 (전체 9개 노드 중 44%)
```

📢 **섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/) 탐색은 대도시 여행 계획이다 — 고속버스(레벨 3)로 큰 도시까지 가고, 시내버스(레벨 1)로 동네까지, 걷기(레벨 0)로 목적지 찾기.

---

## Ⅲ. 삽입과 삭제

### 삽입 (Insert)

```
1. 각 레벨에서 삽입 위치 직전 노드 기록 (update 배열)
2. 동전 던지기로 새 노드 높이 결정
3. 각 레벨에서 연결 포인터 업데이트

새 노드 높이 결정:
  level = 0
  while random() < p and level < max_level:
      level += 1
```

### 삭제 (Delete)

```
1. 각 레벨에서 삭제할 노드 직전 포인터 찾기
2. 해당 레벨의 forward 포인터 건너뛰기
3. 빈 레벨 정리 (max_level 감소)
```

📢 **섹션 요약 비유**: 삽입 시 높이 결정은 계급 진급이다 — 동전 앞면([확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) p)이 나올수록 더 높은 레벨에 등록되고, 뒷면이 나오면 그 계급으로 확정된다.

---

## Ⅳ. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 분석

### [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)

| 연산   | 평균 복잡도  | 최악 복잡도 |
|------|-----------|-----------|
| 탐색  | O(log n)  | O(n)      |
| 삽입  | O(log n)  | O(n)      |
| 삭제  | O(log n)  | O(n)      |

**최악의 경우**: 모든 노드가 레벨 0에만 있을 때 ([확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 낮음)

### AVL 트리 vs [레드-블랙 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/) vs [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)

| 특성         | AVL 트리      | [레드-블랙 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/)  | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)    |
|-----------|------------|--------------|--------------|
| 균형 방식  | 결정적 (회전) | 결정적 (회전+색) | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적       |
| 구현 복잡도 | 높음        | 매우 높음      | 낮음          |
| 메모리     | 낮음        | 낮음           | 높음 (포인터^) |
| [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리  | 어려움      | 어려움         | 유리 (LF 가능)|

📢 **섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)는 "근사치 균형"이다 — AVL처럼 완벽한 균형이 아니라 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 균형에 가깝게 만들어, 복잡한 회전 없이 비슷한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낸다.

---

## Ⅴ. 실제 활용 — [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sorted Set

### [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) ZADD/ZRANGE 구현

```
ZADD scores 90 "Alice"    -> 스킵 리스트에 (key=Alice, score=90) 삽입
ZADD scores 85 "Bob"
ZADD scores 95 "Carol"

ZRANGE scores 0 -1 WITHSCORES
  -> ["Bob" 85, "Alice" 90, "Carol" 95]  // O(k+log n)

ZRANGEBYSCORE scores 85 95
  -> ["Bob", "Alice", "Carol"]           // 범위 검색
```

<strong>Redis가 <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/">스킵 리스트</a>를 선택한 이유</strong>:
1. 범위 검색이 O(k+log n)으로 효율적
2. 구현 단순 -> 유지보수 용이
3. [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 가능성 ([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/) 확장)

📢 **섹션 요약 비유**: Redis의 [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)는 게임 리더보드와 같다 — 점수(score) 기준으로 정렬되어 있고, "90점~95점 사이 플레이어"처럼 범위 조회가 빠르다.

---

## 📌 관련 개념 맵

```
스킵 리스트 (Skip List)
+-- 구조
|   +-- 다중 레벨 연결 리스트
|   +-- 확률적 높이 결정 (동전 던지기)
+-- 연산
|   +-- 탐색 O(log n) 평균
|   +-- 삽입 O(log n) 평균
|   +-- 삭제 O(log n) 평균
+-- 비교 대상
|   +-- AVL 트리 (결정적 균형)
|   +-- 레드-블랙 트리 (결정적)
+-- 실제 사용
    +-- Redis Sorted Set (zset)
    +-- LevelDB MemTable
    +-- Lock-free 동시성 자료구조
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|                스킵 리스트 발전 흐름                             |
+--------------+--------------------+-----------------------------+
| 1990년       | Pugh 논문 발표     | "Skip Lists: A Probabilistic"|
| 2006년       | Redis Sorted Set   | 실제 프로덕션 적용 표준화   |
| 2010년대     | LevelDB / RocksDB  | MemTable 구현에 사용         |
| 2013년       | Lock-free 스킵 리스트 | 동시성 데이터 구조 연구  |
| 2020년대     | 분산 인덱스        | Cassandra 파티션 인덱스       |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
연결 리스트 -> 다중 레벨 -> 스킵 리스트 -> Redis Sorted Set
    v               v             v
O(n) 탐색      O(log n) 평균  ZADD/ZRANGE
    v
AVL/RB 트리와 성능 동등 -> 병렬 처리 우위
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/)는 고속도로가 있는 일반 도로다 — 급하면 고속도로(상위 레벨)로 빠르게 이동하고, 목적지 근처에서 내려(하위 레벨) 정확히 찾는다.
2. 높이 결정은 동전 던지기다 — 앞면이 나오면 계속 올라가고 뒷면이 나오면 멈춘다. 그래서 어떤 노드는 고속도로까지 올라가고, 어떤 노드는 골목길에만 있다.
3. [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 리더보드는 [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/851_skip_list/) 덕분에 빠르다 — "80점~90점 플레이어 모두 보기"처럼 범위 검색을 효율적으로 처리한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 93 / 175

<- **이전**: [단조 스택 (Monotonic Stack) / 단조 큐 (Monotonic Queue)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/092_monotonic_stack/)
**다음**: [KMP (Knuth-Morris-Pratt) 알고리즘](/knowledge-base/studynote/08_algorithm_stats/05_string/094_kmp_algorithm/) ->

---
