+++
title = "24. 스킵 리스트 (Skip List) — 확률적 균형 탐색 구조"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)([Skip List](/knowledge-base/studynote/12_it_management/03_ea_isp/110_skip_list/))는 1990년 William Pugh가 고안한 확률적 자료구조(Probabilistic [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Structure)로, 여러 레벨의 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)([Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/))를 계층화하여 평균 O(log n) 탐색·삽입·삭제를 달성하는 정렬된 딕셔너리(Sorted Dictionary) 구현체다.
> 2. **가치**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 균형 [이진 탐색 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/061_binary_search_tree_bst/)(AVL, [Red-Black Tree](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/))와 동일한 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하면서, 트리 회전(Rotation) 없이 확률적 랜덤화로 균형을 유지하므로 구현이 단순하고 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) 환경에서 [Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/) 구현이 용이하다.
> 3. **판단 포인트**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)의 최악 O(n) 탐색 가능성은 확률에 의존하므로, 최악 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보장이 필요한 시스템에서는 AVL 또는 Red-Black Tree가 적합하다. 반면 Redis의 Sorted Set, LevelDB의 memtable은 [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)의 실무 활용 대표 사례다.

---

## Ⅰ. 개요 및 필요성

정렬된 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)는 탐색이 O(n)으로 느리다. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 이 문제를 여러 레벨의 "고속 레인(Express Lane)"을 추가하여 해결한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스킵 리스트 구조 (값: 1~10 일부)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">레벨3:</div><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">9</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">NIL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">레벨2:</div><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">9</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">NIL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">레벨1:</div><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">7</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">9</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">NIL</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">레벨0:</div><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">4</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">6</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">7</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">8</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">9</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">NIL</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐색 7: 레벨3(1→9 X) → 레벨2(1→5 ok, 5→9 X) →</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">레벨1(5→7 ok!) → 발견 ✓</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비교 횟수: ~4회 vs 연결리스트 7회</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 도시 교통 시스템이다. 모든 골목(레벨0)을 걷는 대신, 도시 고속도로(레벨3)→간선도로(레벨2)→지선(레벨1)→골목 순으로 내려가며 목적지를 빠르게 찾는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 레벨 결정 — 확률적 승진(Probabilistic Promotion)

새 노드 삽입 시 동전 던지기(p=0.5)로 레벨을 결정한다.

```python
def random_level(max_level, p=0.5):
    level = 0
    while random() < p and level < max_level:
        level += 1
    return level
# 레벨0: 100%, 레벨1: 50%, 레벨2: 25%, 레벨3: 12.5%
```

기대 레벨 수: O(log n), 평균 포인터 수: O(n) → 전체 공간 O(n log n) (상수 작음).

### [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)

| 연산 | 평균 | 최악 |
|:---|:---:|:---:|
| 탐색 | O(log n) | O(n) |
| 삽입 | O(log n) | O(n) |
| 삭제 | O(log n) | O(n) |

- **📢 섹션 요약 비유**: 노드의 레벨을 동전 던지기로 정하는 것은 우체국 등급과 같다. 대부분의 우편물(노드)은 일반 배송(레벨0)이지만, 일부는 익일 배송(레벨1), 극소수는 특급(레벨3)으로 올라가 빠른 경로를 만든다.

---

## Ⅲ. 비교 및 연결

| 항목 | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/) | AVL 트리 | Red-Black 트리 |
|:---|:---|:---|:---|
| **평균 탐색** | O(log n) | O(log n) | O(log n) |
| **최악 탐색** | O(n) (확률적) | O(log n) | O(log n) |
| **삽입/삭제** | O(log n) 평균 | O(log n) + 회전 | O(log n) + 회전 |
| **구현 복잡도** | 낮음 | 중간 | 높음 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/">Lock-free</a> 구현</strong> | 용이 | 어려움 | 어려움 |

[Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sorted Set은 내부적으로 [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)를 사용하여 ZADD·ZRANK·ZRANGE 연산을 O(log n)에 처리한다.

- **📢 섹션 요약 비유**: AVL 트리는 무게추가 달린 정밀 저울(엄격한 균형), Red-Black은 규칙이 복잡한 체스, [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 주사위로 균형을 맞추는 즉흥 연주다. 즉흥이지만 평균적으로는 다 비슷하게 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sorted Set 활용
실시간 게임 리더보드 구현.

- `ZADD leaderboard 9800 "player1"` → O(log n) 삽입 (내부 [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)).
- `ZRANK leaderboard "player1"` → 순위 조회 O(log n).
- `ZRANGE leaderboard 0 9 WITHSCORES` → 상위 10명 범위 조회 O(log n + k).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)를 최악 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보장이 필요한 실시간 시스템에 사용하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). p=0.5의 확률로 최악 O(n)이 발생할 수 있으며, 의료·항공 안전 시스템처럼 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 상한 보장이 필요한 경우에는 AVL이나 B-Tree가 적합하다.

- **📢 섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 맑은 날에는 빠른 헬리콥터 배송이지만, 폭풍(최악의 경우)에는 지상 배송으로 바뀔 수 있다. 의료 응급 배송처럼 날씨에 관계없이 정시 도착이 필요하면 다른 수단을 써야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **단순 구현** | 트리 회전 불필요, 코드 간결 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a> 친화</strong> | [Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/) 구현 가능 |
| <strong>범위 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong> | [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 기반 순서 유지 → 범위 탐색 효율 |

[스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 LevelDB·RocksDB의 [memtable](/knowledge-base/studynote/05_database/07_exam_summary/494_memtable_sstable_flush/) 자료구조로 사용되어 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화에 기여하며, CRDTs (Conflict-free Replicated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Types) 등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서도 확률적 자료구조의 활용이 증가하고 있다.

- **📢 섹션 요약 비유**: [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 자연 진화와 같다. 무작위 [돌연변이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/638_mutation_testing_test_case_verification/)(랜덤 레벨 결정)가 평균적으로 최적의 구조를 만들어내며, 인위적인 균형 조정(트리 회전) 없이도 빠른 탐색을 달성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>AVL / <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/">Red-Black Tree</a></strong> | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)의 비교 대상; 최악 보장 균형 트리 |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> Sorted Set</strong> | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/) 실무 활용의 대표 사례 |
| <strong>LevelDB <a href="/knowledge-base/studynote/05_database/07_exam_summary/494_memtable_sstable_flush/">memtable</a></strong> | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/) 기반 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화 자료구조 |
| **확률적 자료구조** | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)가 속하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 패밀리 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/">Lock-free</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a></strong> | [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 장점 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">연결 리스트 — O(n) 탐색, 단순 구조</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스킵 리스트 (1990) — 확률적 레벨, 평균 O(log n)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Redis Sorted Set — 스킵 리스트 실무 적용</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LevelDB / RocksDB memtable — 쓰기 최적화 활용</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Lock-free 스킵 리스트 — 동시성 분산 환경 활용</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. [스킵 리스트](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_skip_list/)는 도서관 책 찾기처럼, 큰 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(레벨3)→중간 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(레벨2)→작은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(레벨1)→실제 책(레벨0) 순으로 점점 좁혀가는 방식이에요!
2. 처음부터 모든 책을 하나씩 뒤지는 대신, 위층 빠른 길을 먼저 타고 내려와서 훨씬 빠르게 찾을 수 있어요.
3. 유명한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) Redis에서 순위표를 빠르게 처리할 때 이 방법을 쓴답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 76 / 175

← **이전**: [23. HashMap vs TreeMap — 해시맵과 트리맵 비교](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/075_hashmap_vs_treemap/)
**다음**: [25. Union-Find (Disjoint Set) — 분리 집합 자료구조](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/077_union_find_disjoint_set/) →

---
