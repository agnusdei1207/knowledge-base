+++
title = "세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트"
date = 2026-03-28

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
- **구간 연산의 최적화**: [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 특정 구간 합, 최솟값, 최댓값 등을 구하는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)와 값 업데이트를 모두 $O(\log n)$ 시간 복잡도에 해결하는 트리 기반 자료구조임.
- <strong>완전 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/">이진 트리</a> 구조</strong>: 리프 노드에는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 개별 요소를 저장하고, 내부 노드에는 자식 노드들의 연산 결과(합, 최소 등)를 저장하여 구간 정보를 계층적으로 관리함.
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> Propagation 확장</strong>: 구간 업데이트가 빈번할 경우 '게으른 전파' 기법을 통해 구간 업데이트 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 $O(\log n)$으로 유지할 수 있는 강력한 확장성을 가짐.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **배경:** 단순 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 구간 합을 구할 때 $O(n)$, 값 변경 시 $O(1)$이 소요됨. 누적 합(Prefix Sum)을 쓰면 구간 합은 $O(1)$이지만 값 변경 시 $O(n)$이 걸림. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실시간으로 변하면서 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 잦은 환경(주식 차트, 게임 랭킹 등)에서는 두 작업 모두 효율적인 자료구조가 필요함.
- **정의:** 주어진 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 구간들을 [이진 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/)의 노드들로 표현하여, 특정 구간에 대한 질의와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수정을 효율적으로 처리하는 자료구조임.
- **특징:** 공간 복잡도는 약 $4n$이며, 트리의 높이가 $\lceil \log_2 n \rceil$으로 제한되어 매우 빠른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보장함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Segment Tree Architecture - Range Sum Example ]

            Node [0-3] (Sum: 20)
           /                    \
    Node [0-1] (Sum: 7)       Node [2-3] (Sum: 13)
     /         \               /         \
Leaf [0] (3)  Leaf [1] (4)  Leaf [2] (6)  Leaf [3] (7)

1. Build: O(n) - Recursive bottom-up approach
2. Query: O(log n) - Traverse overlapping segments
3. Update: O(log n) - Path update from leaf to root

- Index i node children: 2*i (Left), 2*i + 1 (Right)
- Range [L, R] query is split into O(log n) nodes.
```
- **구축 (Build):** 리프 노드에 값을 채우고 부모 노드로 올라오며 구간 연산 결과를 채움.
- **질의 (Query):** 찾고자 하는 구간 $[L, R]$이 현재 노드의 관리 구간과 겹치는지 판단하여, 완전히 포함되면 값을 반환하고 부분 포함되면 자식으로 내려가 결과를 합침.
- **업데이트 (Update):** 특정 인덱스의 값이 바뀌면 해당 리프 노드를 수정하고, 그 인덱스를 포함하는 모든 부모 노드들의 값을 재계산하며 루트까지 올라감.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 단순 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) ([Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)) | 누적 합 (Prefix Sum) | [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) ([Segment Tree](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)) | [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) ([Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)) |
| :--- | :--- | :--- | :--- | :--- |
| <strong>구간 합 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong> | $O(n)$ | $O(1)$ | $O(\log n)$ | $O(\log n)$ |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 수정</strong> | $O(1)$ | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| **메모리 사용** | $n$ | $n$ | $4n$ | $n$ |
| **범용성** | 낮음 | 합계 전용 | 매우 높음 (최소/최대/[GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/) 등) | 중간 (역연산 필요) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **적용 사례:** 실시간 랭킹 시스템의 점수 구간별 사용자 수 집계, 금융 거래 시스템의 특정 기간 가중 평균가 계산, 기하 알고리즘의 평면 스윕(Plane Sweep) 기법.
- **기술사적 판단:** 단순 합계만 필요하고 메모리가 극도로 제한적이라면 [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)가 유리하나, 최솟값/최댓값 등 다양한 연산을 지원해야 하거나 구간 업데이트([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation)가 필수적인 복잡한 비즈니스 로직에서는 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)가 표준 아키텍처임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 동적 변화가 심한 대규모 시스템에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 없이 일관된 구간 정보를 제공함으로써 시스템의 응답성과 신뢰성을 확보함.
- **결론:** [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 알고리즘의 효율성을 극대화하는 핵심 자료구조이며, 현대의 고성능 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 엔진에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성과 속도를 동시에 잡기 위한 필수 기술임.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** [Binary Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/), Range Query [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- **하위/확장 개념:** [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation, [Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/), [Square](/knowledge-base/studynote/04_software_engineering/06_software_architecture/341_iso_iec_25010/) Root Decomposition, 2D [Segment Tree](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)

### 📈 관련 키워드 및 발전 흐름도

```text
[배열 구간 쿼리 — 단순 순회 O(N) 한계]
    |
    v
[세그먼트 트리 (Segment Tree) — 전처리 O(N), 구간 쿼리 O(log N)]
    |
    v
[Lazy Propagation — 구간 업데이트도 O(log N)으로 최적화]
    |
    v
[펜윅 트리 (Fenwick Tree·BIT) — 누적 합 특화, 더 간결한 구현]
    |
    v
[2D 세그먼트 트리·메르지 소트 트리 — 다차원·복합 쿼리 확장]
```
[세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 구간 합·최솟값 같은 구간 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 O(log N)에 처리하며, [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Propagation과 [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)로 발전해 경쟁 프로그래밍의 핵심 자료구조가 되었다.

### 👶 어린이를 위한 3줄 비유 설명
- 여러 칸으로 나뉜 사탕 상자에서 "1번부터 10번 칸까지 사탕이 총 몇 개야?"라고 물었을 때, 일일이 세지 않고 미리 계산해둔 장부를 보고 바로 대답하는 것과 같아요.
- 사탕을 한 칸에 더 넣거나 빼도, 그 칸이 포함된 장부의 숫자만 슥슥 고치면 되니까 아주 편리해요.
- 복잡한 계산을 미리미리 쪼개서 저장해두는 똑똑한 메모장이라고 생각하면 된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 175

<- **이전**: [18. 그래프 (Graph) — 방향/무방향, 가중/비가중](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)
**다음**: [펜윅 트리 / BIT (Fenwick Tree / Binary Indexed Tree) — 구간 합](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/072_fenwick_tree/) ->

---
