+++
title = "21. 퀵 정렬 최적화 — 3-way Partition, Median-of-3 Pivot"
date = 2026-04-02

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

# 거품 정렬 ([Bubble Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

> ⚠️ 이 문서는 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 기초이자 비교 기반(Comparison-based) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 가장 원초적인 형태인 '거품 정렬([Bubble Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/))'의 동작 원리, [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) 한계, 그리고 교육적/이론적 가치를 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 거품 정렬은 인접한 두 원소의 대소 관계를 비교하여 조건에 맞지 않으면 교환(Swap)하는 과정을 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 끝까지 반복함으로써 가장 큰(또는 작은) 원소를 끝으로 밀어내는 '안정 정렬(Stable Sort)' [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: O(N²)이라는 치명적인 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) 탓에 현대 실무 시스템에서는 사용이 완전히 배제되지만, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 비교, 교환, 반복(Loop) 메커니즘을 시각적으로 가장 쉽게 이해할 수 있는 교육적 'Hello World' 역할을 수행한다.
> 3. **융합**: 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 약점(쓸데없는 비교 반복)을 극복하려는 시도에서 [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)) 기법이 파생되었고, 이는 곧 [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)([Insertion Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/))과 칵테일 셰이커 정렬(Cocktail Shaker Sort) 등 발전된 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 사상적 기반이 되었다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

### 1. 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 기초 (The Foundation of Sorting)
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 특정한 기준(오름차순 또는 내림차순)에 따라 재배열하는 '정렬(Sorting)'은 컴퓨터 과학에서 가장 기본적이면서도 중요한 연산입니다. 거품 정렬([Bubble Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/))은 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 순회하면서 인접한 두 원소를 비교하고 교환하는 직관적인 아이디어에서 출발했습니다.
- 원소들이 정렬되면서 큰 값이 마치 거품(Bubble)이 수면 위로 떠 오르는 것처럼 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 오른쪽 끝으로 이동한다고 하여 이름 붙여졌습니다.

### 2. 왜 거품 정렬을 배우는가? (Educational Pain Point)
실제 상용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스나 프로그래밍 언어의 내장 정렬 함수(예: Java의 `Arrays.sort()`, Python의 `Timsort`)에서 거품 정렬을 사용하는 경우는 **0%**에 가깝습니다.
- **필요성**: 그럼에도 불구하고 모든 컴퓨터 과학 커리큘럼에서 거품 정렬을 가르치는 이유는, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 내에서 포인터 이동, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 제어, 임시 변수(Temp)를 이용한 메모리 값 스왑(Swap) 등 **제어문([Control Flow](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/186_control_flow_instructions/))의 근본 원리**를 가장 명확하게 보여주는 '투명한 뼈대'이기 때문입니다.

- **📢 섹션 요약 비유**: 거품 정렬은 "세발자전거"와 같습니다. 아무도 고속도로(빅데이터 환경)에서 세발자전거를 타지는 않지만, 자전거가 어떻게 굴러가는지(정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 뼈대)를 아이들에게 처음 가르칠 때는 이보다 완벽하고 안전한 도구가 없습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) & Mechanism)

### 1. 거품 정렬의 동작 메커니즘 (Step-by-Step)
거품 정렬은 `N`개의 원소를 가진 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 `N-1` 번의 '패스(Pass, 회전)'를 수행합니다. 각 패스마다 인접한 요소 `(A[i], A[i+1])`를 비교하고 정렬 기준을 벗어나면 교환합니다.

```text
┌─────────────────────────────────────────────────────────────┐
│ [ 거품 정렬(Bubble Sort) 동작 과정 - 오름차순 ] │
│ │
│ 초기 배열: [ 5, 3, 8, 4, 2 ] │
│ │
│ [ 1회전 (Pass 1) ] - 가장 큰 수 '8'을 맨 우측으로 밀어냄 │
│ 1) [ 5, 3, 8, 4, 2 ] -> 5 > 3 이므로 Swap -> [ 3, 5, 8, 4, 2 ]│
│ 2) [ 3, 5, 8, 4, 2 ] -> 5 < 8 이므로 Pass -> [ 3, 5, 8, 4, 2 ]│
│ 3) [ 3, 5, 8, 4, 2 ] -> 8 > 4 이므로 Swap -> [ 3, 5, 4, 8, 2 ]│
│ 4) [ 3, 5, 4, 8, 2 ] -> 8 > 2 이므로 Swap -> [ 3, 5, 4, 2, 8*]│
│ │
│ [ 2회전 (Pass 2) ] - 두 번째로 큰 수 '5'를 밀어냄 │
│ 1) [ 3, 5, 4, 2, 8*] -> 3 < 5 이므로 Pass -> [ 3, 5, 4, 2, 8*]│
│ 2) [ 3, 5, 4, 2, 8*] -> 5 > 4 이므로 Swap -> [ 3, 4, 5, 2, 8*]│
│ 3) [ 3, 4, 5, 2, 8*] -> 5 > 2 이므로 Swap -> [ 3, 4, 2, 5*,8*]│
│ │
│ * 이 과정을 총 N-1 번 반복하면 전체가 정렬됨. │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 한 번의 패스가 끝날 때마다 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 맨 오른쪽 끝에는 '현재 정렬되지 않은 원소 중 가장 큰 값'이 고정([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))됩니다. 따라서 2회전에서는 맨 마지막 원소를 비교할 필요가 없고, 3회전에서는 뒤의 2개 원소를 비교할 필요가 없는 방식(검색 범위 축소)으로 최적화됩니다.

### 2. 거품 정렬의 핵심 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)
* **안정 정렬 (Stable Sort)**: 중복된 키 값을 가진 원소들의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상대적 순서가 정렬 후에도 그대로 유지됩니다. (인접한 요소가 완전히 더 클 때만 교환하므로, 같으면 자리 바꿈이 안 일어남)
* **제자리 정렬 (In-place Sort)**: 입력 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 이외에 추가적인 메모리 공간을 거의 요구하지 않습니다. (Swap용 Temp 변수 O(1) 공간만 필요)

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 1. [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) ([Time Complexity](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)) 한계 분석

| 상황 (Case) | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 이유 및 해설 |
| :--- | :--- | :--- |
| **최악 (Worst)** | **O(N²)** | 역순으로 정렬된 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (예: 5,4,3,2,1). 모든 요소를 끝까지 밀어내야 하므로 (N-1) + (N-2) + ... + 1 = N(N-1)/2 번의 비교와 교환 발생. |
| **평균 (Average)**| **O(N²)** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 무작위로 분포된 일반적인 경우. |
| **최선 (Best)** | **O(N)** | 이미 완벽히 정렬된 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)인 경우. 단, 이는 **'[조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/))' [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)** 최적화 코드가 적용되었을 때만 가능. (아래 튜닝 참고) |

### 2. 거품 정렬 vs 다른 O(N²) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (선택/[삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/))
* **vs [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/) ([Selection Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/))**: [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)은 가장 작은 것을 찾아 맨 앞으로 옮길 때 원거리 교환을 하므로 '불안정 정렬'이지만, 거품 정렬은 인접 교환만 하므로 '안정 정렬'입니다. 다만 [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/)은 교환(Swap) 횟수가 O(N)으로 적어 실제로는 거품 정렬보다 미세하게 빠릅니다.
* **vs [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/) ([Insertion Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/))**: [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)은 앞부분이 이미 정렬되어 있다고 가정하고 필요할 때만 비교/교환을 멈춥니다. 거품 정렬은 정렬 상태를 알지 못해 무식하게 끝까지 비교하므로, 거의 정렬된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)이 압도적으로 우수합니다.

- **📢 섹션 요약 비유**: 거품 정렬은 "눈 감고 옆사람 키만 만져보면서 무조건 100번씩 자리를 바꾸는 줄서기"입니다. 줄이 이미 잘 서 있어도 눈을 감고 있으니 무의미하게 계속 만져봐야(비교) 하는 심각한 비효율을 가집니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모** | 정렬해야 할 N의 크기가 수만~수천만 건인가? | O(N²) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)인 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 절대 사용 금지. O(N log N)인 [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/), 병합 정렬, [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/) 도입 필수 |
| **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 정렬 상태** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 이미 99% 정렬되어 있는 상태인가? | 이 경우 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)보다는 **[삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)([Insertion Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/))**이 압도적 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(거의 O(N))을 발휘하므로 아키텍처에 [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/) 채택 |
| **임베디드 메모리**| 칩셋의 메모리가 극도로 부족하여 추가 할당이 불가능한가? | In-place 특성이 중요하지만, 버블보다는 [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)([Heap Sort](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/))이 메모리 소모 없이 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)도 완벽하게 방어하므로 채택 |

*(추가 실무 적용 가이드 - [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) 튜닝)*
만약 레거시 시스템에 부득이하게 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)이 구현되어 있다면, 최소한 **[플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)) 최적화**를 적용해야 합니다.
```java
boolean swapped;
for (int i = 0; i < n - 1; i++) {
swapped = false;
for (int j = 0; j < n - 1 - i; j++) {
if (arr[j] > arr[j+1]) {
swap(arr[j], arr[j+1]);
swapped = true; // 교환이 한 번이라도 일어났음을 기록
}
}
// 이번 회전에서 단 한 번의 교환도 없었다면 이미 완벽히 정렬된 것이므로 즉시 종료!
if (!swapped) break;
}
```

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. 실무 코드에서 거품 정렬 로직이 발견되었다면, 이는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)) 1순위 타겟([기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/))으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고 즉시 Quick/[Merge Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/) 계열 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 함수로 교체해야 합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **학습 도구로서의 영구적 지위**
[버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선 역사에 다시 등장할 확률은 없습니다. 하지만 '어떻게 비효율적인 로직이 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))을 유발하는가'를 설명하는 [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/)(Big-O Notation) 교육의 반면교사() 모델로서, 컴퓨터 공학이 존재하는 한 영원히 첫 챕터에 기록될 것입니다.

2. **변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/): 칵테일 셰이커 정렬 (Cocktail Shaker Sort)**
[버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)의 단점(토끼와 거북이 문제: 큰 값은 빨리 뒤로 가지만 작은 값은 앞으로 느리게 오는 현상)을 개선하기 위해, 왼쪽에서 오른쪽으로 한 번, 오른쪽에서 왼쪽으로 한 번 번갈아가며 거품을 일으키는(양방향 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)) 칵테일 셰이커 정렬로 진화하기도 했습니다.

- **📢 섹션 요약 비유**: 거품 정렬은 "박물관에 전시된 인류 최초의 돌도끼"입니다. 오늘날 나무를 벨 때 돌도끼를 쓰는 사람은 없지만, 전기톱이 어떤 원리로 탄생했는지 알려주는 훌륭한 역사적 가치를 품고 있습니다.

---

## 🧠 지식 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

* **정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) (Sorting Algorithms)**
* **O(N²) 계열 (단순/비효율)**: **거품 정렬**, [선택 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/), [삽입 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/052_insertion_sort_algorithm/)
* **O(N log N) 계열 (고속/실무용)**: [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/), 병합 정렬, [힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)
* **O(N) 계열 (비비교 정렬)**: [기수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)([Radix](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/)), [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)(Counting)
* **[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 주요 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)**
* 제자리 정렬 (In-place) - O(1) [공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)
* 안정 정렬 (Stable) - 중복 키 순서 보존
* **[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 기법**
* [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) ([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)) - 최선 O(N) 방어

---

### 📈 관련 키워드 및 발전 흐름도

```text
[버블 정렬 (Bubble Sort) — O(N²) 단순 비교 교환]
│
▼
[선택 정렬 / 삽입 정렬 — O(N²) 계열 단순 알고리즘]
│
▼
[퀵 정렬 (Quick Sort) — 평균 O(N log N), 실무 표준]
│
▼
[병합 정렬 (Merge Sort) — O(N log N) 안정 정렬]
│
▼
[기수 정렬 (Radix Sort) — O(N) 비비교 정렬 (특수 조건)]
```
[버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 O(N²)의 비효율적 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이지만 정렬 이론의 원점이며, 실무에서는 평균 O(N log N)의 퀵·병합 정렬이 표준이고 특수 조건에서는 O(N) [기수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/017_radix_sort/)로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명
1. [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 큰 숫자가 거품처럼 뒤로 뽀글뽀글 올라가는 정렬이에요 — 제일 큰 숫자부터 이웃끼리 자리를 바꿔가며 줄을 세우는 방법이죠!
2. 100명을 줄 세울 때 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 최대 4,950번 자리를 바꿔야 하지만, [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)은 약 700번만 해도 돼요 — 그래서 실제 컴퓨터는 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)을 거의 안 써요.
3. 그래도 [버블 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)은 "정렬이 무엇인가"를 가르쳐주는 가장 이해하기 쉬운 교과서 같은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이랍니다!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/):** 본 문서는 구조적 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 및 보완되었습니다. (Verified at: 2026-04-02)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 175

← **이전**: [20. 퀵 정렬 (Quick Sort) — 평균 O(n log n), 최악 O(n²), 불안정](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)
**다음**: [21. 해밀턴 경로 (Hamiltonian Path) — NP-완전, 백트래킹](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/049_hamiltonian_path/) →

---
