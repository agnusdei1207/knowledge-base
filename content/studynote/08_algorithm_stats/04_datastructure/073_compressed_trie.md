---
title: "Compressed Trie / Patricia Trie"
date: "2024-03-24"
tags:
  - "studynote-algorithm"
---

## 핵심 인사이트 (3줄 요약)
1. **공간 효율성 극대화**: 일반 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)([Trie](/studynote/08_algorithm_stats/04_datastructure/066_trie/))의 단일 자식 노드들을 하나의 간선으로 병합하여 메모리 낭비를 획기적으로 줄인 자료구조입니다.
2. <strong>패트리샤 트리 (Patricia <a href="/studynote/08_algorithm_stats/04_datastructure/066_trie/">Trie</a>)</strong>: 'Practical [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) to Retrieve Information Coded in Alphanumeric'의 약자로, [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 비교를 통해 검색 속도를 최적화합니다.
3. <strong>결정적 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: 문자열 길이에 비례하는 O(L) 검색 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하면서도, 노드 수를 최소화하여 대규모 사전 검색 및 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블에 적합합니다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
일반적인 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)는 모든 문자를 개별 노드로 저장하므로, 'apple', 'apply'와 같이 공통 접두사가 길거나 자식이 하나뿐인 경로가 많을 때 심각한 메모리 파편화와 낭비가 발생합니다. <strong><a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>된 <a href="/studynote/08_algorithm_stats/04_datastructure/087_trie/">트라이</a>(Compressed <a href="/studynote/08_algorithm_stats/04_datastructure/066_trie/">Trie</a>)</strong>는 이러한 불필요한 단일 노드 연쇄를 하나의 노드로 합쳐 트리 높이를 낮추고 [공간 복잡도](/studynote/08_algorithm_stats/01_basics/003_space_complexity/)를 개선한 변형 자료구조입니다. 특히 바이너리 환경에서 구현된 패트리샤 트리는 디지털 트리 탐색의 표준으로 활용됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[압축](/studynote/02_operating_system/06_memory_management/347_compaction/)된 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)의 핵심은 <strong>"자식이 하나인 내부 노드의 제거"</strong>입니다. 각 노드는 문자 하나가 아닌, 문자열 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)(Label)를 저장합니다.

```text
[ Compressed Trie Architecture Concept ]

Standard Trie:        Compressed Trie (Patricia):
     (root)                 (root)
       |                      |
       a                    "appl"
       |                    /    \
       p                 "e"      "y"
       |                (end)     (end)
       p
       |
       l
      / \
     e   y
   (end)(end)

<Bilingual Components>
- Edge Label (간선 레이블): 문자열의 부분 조각을 저장 (Stores string segments)
- Internal Node (내부 노드): 분기점 발생 시에만 생성 (Created only at branching points)
- External Node (외부 노드/단말): 문자열의 끝을 표시 (Indicates end of string)
```

**핵심 메커니즘:**
1. **노드 병합(Node Merging)**: 자식이 하나뿐인 경로는 접두사로 묶어 단일 노드로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/).
2. <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 비교(<a href="/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">Bit</a> Comparison)</strong>: 패트리샤 트리의 경우, 차이가 발생하는 첫 번째 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 위치([Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))를 기반으로 분기하여 비교 횟수 최소화.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 일반 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/) (Standard [Trie](/studynote/08_algorithm_stats/04_datastructure/066_trie/)) | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/) (Compressed [Trie](/studynote/08_algorithm_stats/04_datastructure/066_trie/)) | [해시 테이블](/studynote/08_algorithm_stats/04_datastructure/067_hash_table/) ([Hash Table](/studynote/08_algorithm_stats/04_datastructure/067_hash_table/)) |
|:---:|:---:|:---:|:---:|
| <strong><a href="/studynote/08_algorithm_stats/01_basics/003_space_complexity/">공간 복잡도</a></strong> | O(Σ size of strings) - 높음 | O(N) - 노드 수 비례 (최적) | O(N) - 버킷 낭비 가능성 |
| **검색 속도** | O(L) - 문자열 길이 | O(L) - 문자열 길이 | O(1) - 평균 (최악 O(N)) |
| **범위 검색** | 지원 (Excellent) | 지원 (Very Good) | 미지원 (Poor) |
| **구현 난이도** | 낮음 | 중간 (노드 분할/병합 로직 필요) | 중간 |
| **주요 용도** | 단순 사전, 자동완성 | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블, IP 검색, 대용량 사전 | 일반적인 키-값 저장 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
<strong>실무 적용 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>:</strong>
- <strong>네트워크 <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong>: IP 주소의 Longest Prefix Match(LPM)를 구현할 때 가장 효율적입니다.
- <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템</strong>: 디렉토리 구조나 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로 검색 시 공통 접두사를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하여 메모리 점유율을 낮춥니다.
- **이더리움 머클 패트리샤 트리 (MPT)**: [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에서 상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하고 무결성을 검증하는 핵심 구조로 사용됩니다.

**기술사적 판단:**
"단순히 메모리를 아끼는 것을 넘어, CPU 캐시 지역성(Cache Locality)을 향상시켜 실제 검색 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 가속화합니다. 하지만 빈번한 삽입/삭제가 발생하는 환경에서는 노드를 쪼개고 합치는 오버헤드가 발생하므로, 정적인 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이나 읽기 위주의 서비스에 우선적으로 고려해야 합니다."

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[압축](/studynote/02_operating_system/06_memory_management/347_compaction/)된 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집약적 컴퓨팅 환경에서 <strong>'공간과 속도의 최적 균형'</strong>을 제공합니다. 최근 생성형 AI의 [토큰화](/studynote/09_security/16_data_privacy/820_tokenization/)([Tokenization](/studynote/09_security/16_data_privacy/820_tokenization/)) 과정이나 대규모 인덱싱 엔진에서 메모리 계층 구조를 효율적으로 활용하기 위한 필수 도구로 재조명받고 있습니다. 결론적으로, 구조적 간결함을 통해 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 탐색 효율을 극대화하는 표준 자료구조입니다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [Trie](/studynote/08_algorithm_stats/04_datastructure/066_trie/), [Radix](/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) Tree
- **유사 개념**: Crit-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Tree, Compact Prefix Tree
- **하위 기술**: Merkle Patricia Tree (MPT), Adaptive [Radix](/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) Tree ([ART](/studynote/02_operating_system/10_security/621_art_android_runtime/))

### 📈 관련 키워드 및 발전 흐름도

```text
[일반 트라이 (Standard Trie — 문자 단위 노드)]
    |
    v
[압축 트라이 / 기수 트리 (Compressed Trie / Radix Tree)]
    |
    v
[Patricia Trie — 단일 자식 노드 완전 제거]
    |
    v
[Merkle Patricia Tree (MPT — 이더리움 상태 저장)]
    |
    v
[Adaptive Radix Tree (ART — 인메모리 DB 인덱스)]
```
단순 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)의 노드 폭증 문제를 경로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)으로 해결한 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)는 IP [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템·[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) MPT 등에서 공간과 캐시 효율의 최적 균형을 제공한다.

### 👶 어린이를 위한 3줄 비유 설명
1. 일반 [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)가 한 글자씩 써진 계단을 하나씩 밟고 올라가는 거라면,
2. [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [트라이](/studynote/08_algorithm_stats/04_datastructure/087_trie/)는 똑같은 글자가 계속될 때 그 계단들을 엘리베이터처럼 한 번에 슝~ 지나가는 거예요.
3. 덕분에 훨씬 빨리 꼭대기(단어 끝)에 도착하고, 계단도 적게 만들어서 땅을 아낄 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 175

<- **이전**: [펜윅 트리 / BIT (Fenwick Tree / Binary Indexed Tree) — 구간 합](/studynote/08_algorithm_stats/04_datastructure/072_fenwick_tree/)
**다음**: [22. 서픽스 트리/배열 (Suffix Tree/Array) — 문자열 분석](/studynote/08_algorithm_stats/04_datastructure/074_suffix_tree_array/) ->

---
