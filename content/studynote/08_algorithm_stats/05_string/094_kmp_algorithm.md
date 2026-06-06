---
title: "094. Kmp Algorithm"
date: "2024-03-21"
tags:
  - "studynote-algorithm"
---

## 핵심 인사이트 (3줄 요약)
1. **불필요한 비교 제거**: 문자열 매칭 실패 시 이미 비교한 정보를 활용하여 패턴의 시작점을 효율적으로 건너뛰는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)임.
2. **실패 함수 (LPS) 활용**: 접두사와 접미사가 일치하는 최대 길이를 미리 계산하여(Failure Function) $O(N+M)$의 [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)를 달성함.
3. **결정적 유한 오토마타 (DFA) 원리**: 문자열 탐색을 상태 전이로 최적화하여 최악의 경우에도 선형 시간을 보장하는 기술사적 핵심 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)임.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **개념**: 텍스트(Text)에서 패턴(Pattern)을 찾을 때, 매칭이 실패한 지점까지의 정보를 재사용하여 탐색 효율을 극대화한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)임.
- **배경**: 단순 비교(Brute-force) 방식은 최악의 경우 $O(N \times M)$이 소요되어 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리에 부적합함. 이를 해결하기 위해 Knuth, Morris, Pratt가 공동 개발함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
#### 1. KMP [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 메커니즘
- <strong>LPS (Longest Proper Prefix which is also Suffix) <a href="/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a></strong>: 패턴 내부에서 중복되는 하위 패턴을 찾아 매칭 실패 시 되돌아갈 위치를 지정함.

```text
[ KMP Matching Logic & LPS Table ]
Text:    A B A B C A B A B A B D
Pattern: A B A B A B D
         | | | | | x (Mismatch at index 4)

[ LPS Array Construction ]
Pattern: A B A B A B D
Index:   0 1 2 3 4 5 6
LPS:     0 0 1 2 3 4 0  <-- Prefix matching suffix lengths

[ State Transition Logic ]
(State) ---[Match]--> (Next State)
   |
[Mismatch]
   |
   V
(Backtrack to LPS[index-1])
```

#### 2. [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) 분석
- **LPS 계산**: 패턴 길이 $M$에 대해 $O(M)$ 소요.
- **매칭 과정**: 텍스트 길이 $N$에 대해 포인터를 뒤로 돌리지 않고 전진하므로 $O(N)$ 소요.
- **최종**: $O(N+M)$.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 단순 비교 (Naive) | KMP [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [보이어-무어](/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/) ([Boyer-Moore](/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/)) |
| :--- | :--- | :--- | :--- |
| <strong><a href="/studynote/08_algorithm_stats/01_basics/002_time_complexity/">시간 복잡도</a></strong> | $O(N \times M)$ | $O(N + M)$ | $O(N/M) \sim O(N \times M)$ |
| **탐색 방향** | 왼쪽 -> 오른쪽 | 왼쪽 -> 오른쪽 | 오른쪽 -> 왼쪽 (Backwards) |
| **주요 특징** | 구현이 단순함 | 최악의 경우에도 선형 시간 보장 | 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 가장 우수함 (스킵 큼) |
| **추가 공간** | $O(1)$ | $O(M)$ - LPS [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) | $O(\Sigma + M)$ - Skip Tables |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **실무 적용**: 검색 엔진의 키워드 매칭, DNA 염기 서열 분석, [바이러스](/studynote/02_operating_system/10_security/589_virus/) 패턴 탐지(Signature Matching) 등에서 핵심적으로 활용됨.
- **기술사적 판단**: KMP는 이론적으로 선형 시간을 보장한다는 점에서 안정적이지만, 실제 문자열의 집합이 크고 패턴이 긴 경우 [보이어-무어](/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 더 선호될 수 있음. 그러나 하드웨어 레벨의 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 시에는 포인터를 되돌리지 않는 KMP가 더 효율적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 대규모 텍스트 [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/) 시 처리 속도를 비약적으로 향상시키며, 실시간 탐색 시스템의 응답 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 보장함.
- **결론**: KMP는 정보이론과 오토마타 이론이 결합된 우아한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 최적화의 기본 소양이며 표준 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 구현의 기반이 됨.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: 문자열 탐색 (String Searching), [동적 프로그래밍](/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) (LPS 계산 시 활용)
- **유사 개념**: [Aho-Corasick](/studynote/08_algorithm_stats/05_string/098_aho_corasick/) (다중 패턴 KMP), [Rabin-Karp](/studynote/08_algorithm_stats/05_string/096_rabin_karp_algorithm/) (해싱 활용)
- **응용 분야**: NLP(자연어 처리), 생물정보학, [침입 탐지 시스템](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)([IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/))

### 📈 관련 키워드 및 발전 흐름도

```text
[Naive 문자열 매칭]
    |
    v
[부분 일치 테이블]
    |
    v
[KMP 알고리즘]
    |
    v
[선형 시간 검색]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 숨바꼭질을 할 때, 틀린 곳을 다시 찾아보지 않고 "아까 여기까지는 맞았지!"라고 기억해두는 영리한 방법이에요.
2. 노래 가사에서 "사랑"이라는 글자를 찾을 때, "사" 다음이 "람"이면 다시 처음부터 안 찾고 다음 "사"를 바로 찾아가는 거예요.
3. 똑같은 실수를 반복하지 않게 미리 '실패할 때 어디로 갈지' 지도를 그려놓는 것과 같아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 94 / 175

<- **이전**: [스킵 리스트 (Skip List)](/studynote/08_algorithm_stats/04_datastructure/093_skip_list/)
**다음**: [보이어-무어 (Boyer-Moore) 알고리즘](/studynote/08_algorithm_stats/05_string/095_boyer_moore_algorithm/) ->

---
