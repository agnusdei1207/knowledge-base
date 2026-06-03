+++
title = "29. 세그먼트 트리 (Segment Tree)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)([Segment Tree](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/))는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(범위 합, 최솟값, 최댓값, [GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/))와 점 업데이트를 O(log n)에 처리하는 완전 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/) 자료구조다. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)으로 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 구성한다.
> 2. **가치**: 구간 합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 단순 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)로 처리하면 O(n), 누적 합(Prefix Sum)으로는 O(1) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)지만 O(n) 업데이트. [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)와 업데이트 모두 O(log n)으로 균형을 맞춘다. 업데이트가 빈번한 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 문제의 표준 해법이다.
> 3. **판단 포인트**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) vs [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)([BIT](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)) — BIT는 구현이 간단하고 상수 인자가 작지만 구간 최솟값 등 특정 연산은 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)만 가능하다. 레이지 프로파게이션([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation)은 구간 업데이트가 필요할 때 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)에 추가하는 핵심 최적화다.

---

## Ⅰ. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│         세그먼트 트리 구조 (배열 합)                       │
├──────────────────────────────────────────────────────────┤
│  배열: [1, 3, 5, 7, 9, 11]                               │
│                                                           │
│              [36]       ← 전체 합 (인덱스 1)             │
│            /       \                                     │
│         [16]       [20]  ← 좌우 절반                     │
│        /    \     /    \                                  │
│      [4]   [12] [9]  [11] ← 쿼터                        │
│     /  \  /  \  /  \                                     │
│   [1] [3][5][7][9][11] ← 리프 노드 (원소)                │
│                                                           │
│  구간 합 [1..4]: 루트→[16]→[4]+[12] = 16 → O(log n)      │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 회사 조직도 합산이다. CEO(루트)는 전체 합을 알고, 부장(중간 노드)은 자기 팀 합을 알며, 직원(리프)은 자신의 값을 안다. 특정 팀 합을 알려면 최소한의 상사만 물어보면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구현 ([배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 기반)

```python
class SegmentTree:
    def __init__(self, arr):
        n = len(arr)
        self.tree = [0] * (4 * n)
        self.build(arr, 0, n-1, 1)
    
    def build(self, arr, l, r, node):
        if l == r:
            self.tree[node] = arr[l]
            return
        mid = (l + r) // 2
        self.build(arr, l, mid, 2*node)
        self.build(arr, mid+1, r, 2*node+1)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def query(self, l, r, node, nl, nr):  # 구간 합 O(log n)
        if r < nl or nr < l: return 0
        if l <= nl and nr <= r: return self.tree[node]
        mid = (nl + nr) // 2
        return self.query(l, r, 2*node, nl, mid) +                self.query(l, r, 2*node+1, mid+1, nr)
```

### 레이지 프로파게이션 ([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation)

```text
문제: 구간 [l, r] 전체에 +k 업데이트 → 순진하게 하면 O(n)
해결: 업데이트를 지연(lazy) 저장 → 필요할 때만 전파
→ 구간 업데이트도 O(log n) 가능
```

- **📢 섹션 요약 비유**: 레이지 프로파게이션은 일괄 업무 처리다. 100명 직원 급여를 일일이 바꾸는 대신, "팀 전체 +[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 인상" 메모만 남겨두고 실제 계산은 각 직원 급여를 조회할 때만 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) | 누적 합 | [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) | [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) |
|:---|:---|:---|:---|:---|
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | O(n) | O(1) | O(log n) | O(log n) |
| 업데이트 | O(1) | O(n) | O(log n) | O(log n) |
| 구현 | 쉬움 | 쉬움 | 복잡 | 간단 |
| 구간 최솟값 | O(n) | ❌ | O(log n) | 어려움 |

- **📢 섹션 요약 비유**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 빠른 인터넷 뱅킹이다. 잔액 조회([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))와 입금(업데이트) 모두 빠르게 처리할 수 있어, 조회만 빠른 장부(누적 합)나 입금만 빠른 장부([배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))보다 균형잡힌 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 응용 문제

```text
구간 최솟값 (Range Minimum Query):
  세그먼트 트리 리프 = 원소, 내부 = min(자식)
  → 구간 최솟값 O(log n), 업데이트 O(log n)

구간 최솟값 + Offline: 스파스 테이블 (O(1) 쿼리, O(n log n) 전처리)

구간 업데이트 + 구간 합: 레이지 프로파게이션 필수

지속 세그먼트 트리 (Persistent Segment Tree):
  시간축 버전 관리 → 과거 시점 쿼리 O(log n)
  → 오프라인 쿼리, K번째 원소 찾기
```

- **📢 섹션 요약 비유**: 지속 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 시간 여행 가능한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)다. 트리의 모든 과거 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 O(log n) 공간으로 유지해서 "3단계 전 상태의 구간 합이 얼마였나?"를 빠르게 조회할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong>균형 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·업데이트 모두 O(log n) |
| **범용성** | 합·최소·최대·[GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/) 등 다양한 연산 |
| **확장성** | 레이지·지속 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)로 기능 확장 |

[세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 기술 면접과 경쟁 프로그래밍의 핵심 자료구조다. Java TreeMap, Python Sorted Containers, C++ segment_tree(custom) 등으로 구현하며, DB 인덱싱·범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화의 원리적 기반이 된다.

- **📢 섹션 요약 비유**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) B-트리의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다. B-트리가 디스크 기반 범위 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 최적화하듯, [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 메모리 내 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 최적화한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">펜윅 트리</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">BIT</a>)</strong> | [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) 간소화 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/">스파스 테이블</a></strong> | 정적 구간 최솟값 O(1) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **레이지 프로파게이션** | 구간 업데이트 최적화 |
| <strong>지속 <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/">세그먼트 트리</a></strong> | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리·시간축 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/">분할 정복</a></strong> | [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)의 설계 원리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[배열 선형 탐색 — 구간 쿼리 O(n)]
    │
    ▼
[누적 합 — 정적 구간 합 O(1) 쿼리]
    │
    ▼
[세그먼트 트리 — 동적 구간 쿼리·업데이트 O(log n)]
    │
    ▼
[레이지 프로파게이션 — 구간 업데이트 O(log n)]
    │
    ▼
[지속 세그먼트 트리 — 시간축 버전 관리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 회사 조직도예요! CEO(루트)는 전체 합을 알고, 팀장은 팀 합을, 직원은 자기 값을 알아요.
2. 구간 합·최솟값 조회와 값 업데이트를 모두 O(log n)으로 빠르게 처리할 수 있어요!
3. 레이지 프로파게이션은 "팀 전체 급여 +[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%" 메모만 남겨두고 나중에 계산하는 스마트 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 업데이트예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 175

← **이전**: [29. 덱 (Deque — Double-Ended Queue)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/)
**다음**: [30. 펜윅 트리 (BIT) — 범위 합 쿼리의 효율적 구조](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) →

---
