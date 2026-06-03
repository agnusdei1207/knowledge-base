+++
title = "펜윅 트리 / BIT (Fenwick Tree / Binary Indexed Tree) — 구간 합"
date = 2026-03-28

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
- **[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산을 이용한 구간 합 최적화**: 2진수의 마지막 1비트(`i & -i`)가 관리하는 구간의 길이를 결정하는 원리를 이용하여 구간 합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)와 값 업데이트를 모두 $O(\log n)$에 처리함.
- **메모리 효율성 극대화**: [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)가 약 $4n$의 공간을 필요로 하는 것과 달리, 원본 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)과 동일한 $n$의 공간만 사용하여 매우 경제적임.
- **역연산 가능 연산에 특화**: 구간 합(Sum)과 같이 역연산이 존재하는 경우에 가장 효율적이며, 구현이 매우 단순하여 실무 적용이 용이함.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **배경:** [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 강력하지만 구현이 복잡하고 메모리 사용량이 많음. 1994년 피터 펜윅(Peter Fenwick)이 제안한 이 자료구조는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 조작을 통해 트리의 구조를 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 하나로 압축하여 성능과 효율성을 동시에 확보함.
- **정의:** 각 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 2진수로 표현했을 때, 가장 낮은 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([LSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/079_lsb/))가 담당하는 구간의 합을 저장하는 방식으로 구성된 자료구조임.
- **별칭:** 2진 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 트리(Binary [Indexed](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) Tree, [BIT](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/))라고도 불림.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Fenwick Tree (BIT) Structure - Indexing Logic ]

Original Array: [A1, A2, A3, A4, A5, A6, A7, A8]
BIT Array (T):  [T1, T2, T3, T4, T5, T6, T7, T8]

Representation:
T1: A1 (1=0001, manages 1)
T2: A1+A2 (2=0010, manages 2)
T4: A1+A2+A3+A4 (4=0100, manages 4)
T6: A5+A6 (6=0110, manages 2)
T8: A1+A2+A3+A4+A5+A6+A7+A8 (8=1000, manages 8)

Operation:
1. Update i: i += (i & -i) while i <= n
2. Prefix Sum i: i -= (i & -i) while i > 0
```
- **핵심 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산:** `i & -i`는 $i$를 2진수로 나타냈을 때 가장 오른쪽에 있는 1의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)값([LSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/079_lsb/))을 반환함 (예: $6(0110) \rightarrow 2(0010)$).
- **업데이트:** [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) $i$의 값을 $X$만큼 늘릴 때, $i$를 포함하는 모든 상위 관리 노드들의 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)는 $i$에 LSB를 계속 더해가며 찾음.
- **[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/):** $1$부터 $i$까지의 합(Prefix Sum)은 $i$에서 LSB를 계속 빼가며 만나는 노드들의 값을 합산함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/) ([Segment Tree](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)) | [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) ([Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)) |
| :--- | :--- | :--- |
| **[시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)** | $O(\log n)$ | $O(\log n)$ |
| **[공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)** | $4n$ | $n$ (원본 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기) |
| **구현 난이도** | 높음 ([재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)/복잡) | 매우 낮음 (반복문/[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)연산) |
| **범용성** | 매우 높음 (Min/Max/Sum/[GCD](/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/)) | 중간 (역연산 존재 시 유리) |
| **상수 시간** | 상대적으로 느림 | 매우 빠름 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **적용 사례:** 대규모 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 데이터의 실시간 빈도수 집계, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 구간 합 최적화, 온라인 저지 시스템의 순위 변동 계산.
- **기술사적 판단:** 구간 합(Range Sum) 위주의 작업이면서 메모리 절약과 구현 속도가 중요한 임베디드 시스템이나 실시간 대용량 트래픽 처리 환경에서는 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)보다 [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)가 최선의 엔지니어링 선택임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 하드웨어 친화적인 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산을 통해 연산 오버헤드를 최소화하고, 메모리 제약이 심한 환경에서도 고성능 구간 연산을 가능하게 함.
- **결론:** [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)는 "단순함이 복잡함을 이긴다"는 것을 보여주는 대표적 사례이며, [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산의 마법을 통해 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 효율성의 한계를 돌파한 걸작임.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념:** Prefix Sum, Range Query [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- **하위/확장 개념:** 2D [Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/), Range Update [Fenwick Tree](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/), Lowest Significant [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) ([LSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/079_lsb/))

### 📈 관련 키워드 및 발전 흐름도

```text
[선형 누적합 (Prefix Sum Array) — O(N) 전처리, O(1) 구간 조회]
    │
    ▼
[세그먼트 트리 (Segment Tree) — O(log N) 구간 갱신/조회, O(N) 공간]
    │
    ▼
[펜윅 트리 / BIT (Binary Indexed Tree) — LSB 기반, O(log N) 갱신+조회, 절반 공간]
    │
    ▼
[2D 펜윅 트리 — 행렬 구간 합/업데이트로 확장]
    │
    ▼
[Range Update Fenwick Tree — 구간 업데이트·포인트 쿼리로 변형 응용]
```
누적합 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 O(N) 갱신 한계를 극복하고자 [세그먼트 트리](/knowledge-base/studynote/12_it_management/02_itsm_itil/075_combinatorics/)가 등장했고, 더 적은 공간에 [LSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/079_lsb/) 트릭을 활용한 [펜윅 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)가 실무 표준으로 자리 잡았다.

### 👶 어린이를 위한 3줄 비유 설명
- 한 번에 1층, 2층, 4층씩 훌쩍 뛰어넘는 거인 발자국처럼 숫자를 관리하는 방법이에요.
- 장부의 숫자 하나를 고치면, 그 숫자가 들어간 더 큰 장부들도 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산이라는 '마법의 지팡이'로 한 번에 슥슥 고쳐요.
- 종이(메모리)를 아주 조금만 쓰면서도 계산은 슈퍼 컴퓨터처럼 빠르게 할 수 있는 최고의 비법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 175

← **이전**: [세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/071_segment_tree/)
**다음**: [압축된 트라이 (Compressed Trie / Patricia Trie)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/073_compressed_trie/) →

---
