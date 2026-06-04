---
title: "75. 세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트"
tags:
  - "it_management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 세그먼트 트리 ([Segment](/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Tree)는 구간을 반으로 쪼개며 각 구간의 요약값을 저장해, 범위 질의와 갱신을 둘 다 O(log n) 수준으로 처리하는 자료구조다.
> 2. **가치**: prefix sum은 업데이트에 약하고 완전 탐색은 느리다. 세그먼트 트리는 둘 사이의 균형을 맞춰 동적 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 구간 합·최솟값·최댓값을 안정적으로 다룬다.
> 3. **판단 포인트**: 결합법칙이 성립하는 연산이면 거의 다 얹을 수 있지만, 메모리 4n 정도를 감수해야 하므로 작은 문제에 과하게 쓰면 오히려 손해다.

---

## Ⅰ. 개요 및 필요성

세그먼트 트리는 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 전체를 한 번에 보지 않고, 반씩 쪼갠 구간을 트리로 저장한다. 그래서 어떤 범위를 묻더라도 해당 구간을 덮는 노드만 따라가면 된다.

이 구조가 필요한 이유는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 자주 바뀌기 때문이다. prefix sum은 빠르지만 값이 바뀔 때마다 다시 계산해야 하고, 완전 탐색은 갱신과 질의가 모두 느리다. 세그먼트 트리는 이 둘의 중간에서 동적 질의에 강해진다.

```text
       [1..8]
     /                      [1..4]    [5..8]
  /   \      /              [1..2] [3..4] [5..6] [7..8]
```

각 노드는 자신이 담당하는 구간의 요약값을 들고 있으므로, 전체를 다시 보지 않아도 된다.

- **📢 섹션 요약 비유**: 책 한 권이 아니라 목차를 먼저 보는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

세그먼트 트리의 핵심은 분할과 병합이다. 노드는 구간의 대표값을 저장하고, 질의는 겹치는 구간만 내려가며, 갱신은 바뀐 경로만 다시 계산한다.

| 동작 | [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 핵심 |
| :--- | :--- | :--- |
| Build | O(n) | 바닥에서 위로 합침 |
| Query | O(log n) | 필요한 구간만 탐색 |
| Point Update | O(log n) | 경로 재계산 |
| [Lazy](/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation | O(log n) | 범위 갱신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |

연산이 합쳐질 수만 있다면 sum, min, max, gcd처럼 여러 문제에 적용된다. 반대로 결합법칙이 깨지는 연산은 세그먼트 트리에 잘 맞지 않는다.

- **📢 섹션 요약 비유**: 구간별 요약 노트를 쌓아 두는 책장이다.

---

## Ⅲ. 비교 및 연결

세그먼트 트리는 prefix sum, [Fenwick Tree](/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) (Binary [Indexed](/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) Tree), Sparse Table과 자주 비교된다. 정적 합만 필요하면 prefix sum이 가장 단순하고, 점 갱신이 많으면 세그먼트 트리나 Fenwick Tree가 유리하다.

| 비교 축 | [Segment](/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Tree | [Fenwick Tree](/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) | [Sparse Table](/studynote/08_algorithm_stats/04_datastructure/081_sparse_table/) |
| :--- | :--- | :--- | :--- |
| 갱신 | 강함 | 강함 | 약함 |
| 범위 질의 | 강함 | 누적형에 강함 | 매우 강함(정적) |
| 메모리 | 큼 | 작음 | 큼 |
| 활용도 | 높음 | 높음 | 정적 질의 전용 |

따라서 경계는 "업데이트가 있느냐"와 "질의가 정적이냐"다. 이 질문에 따라 자료구조 선택이 거의 결정된다.

- **📢 섹션 요약 비유**: 간단한 질문엔 메모장이, 자주 바뀌면 장부가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무적으로는 범위 질의와 범위 갱신이 동시에 있을 때 세그먼트 트리를 검토한다. 예를 들어 구간 합, 구간 최소, [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 충돌, 통계 집계처럼 "쪼갠 뒤 다시 합치는" 문제에 적합하다.

체크 포인트는 다음과 같다.
- 연산이 결합법칙을 만족하는가.
- 인덱스가 커서 4n 메모리를 감당할 수 있는가.
- [lazy](/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) propagation이 정말 필요한가.

안티패턴은 정적 문제에 과하게 쓰는 것이다. 질문이 단순하다면 prefix sum이 더 낫고, 희소한 인덱스라면 먼저 coordinate compression을 생각해야 한다.

- **📢 섹션 요약 비유**: 모든 문제에 장부를 쓰면 책상이 넘친다.

---

## Ⅴ. 기대효과 및 결론

세그먼트 트리는 "구간을 요약하는 사고"를 코드로 만든 것이다. 그래서 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)을 단순 저장 공간이 아니라 계층적 정보 구조로 보게 만든다.

결론은 단순하다. 업데이트가 없으면 더 가벼운 방법을 쓰고, 업데이트가 많고 연산이 합쳐질 수 있으면 세그먼트 트리를 쓴다. 이 기준만 잡아도 자료구조 선택이 훨씬 명확해진다.

- **📢 섹션 요약 비유**: 구간별 메모를 만들어 두면 긴 책도 빨리 찾는다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) | 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| Node | 구간 요약값 |
| Merge | 왼쪽+오른쪽 결합 |
| [Lazy](/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) | 범위 갱신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| Query / Update | 질의와 수정 |

### 관련 키워드 및 발전 흐름도

```text
build
  |
  v
choose interval
  |
  v
descend tree
  |
  v
merge answers
  |
  v
return result
```

### 어린이를 위한 3줄 비유 설명

1. 책장마다 요약 메모를 붙여 두면 찾기 쉬워요.
2. 어느 칸이 바뀌면 그 근처 메모만 다시 쓰면 돼요.
3. 그래서 큰 책장도 빨리 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 587

<- **이전**: [74. 순열과 조합 (Permutation and Combination)](/studynote/12_it_management/02_itsm_itil/858_permutation_combination/)
**다음**: [75. 인시던트 관리 (Incident Management)](/studynote/12_it_management/02_itsm_itil/859_incident_management/) ->

---
