+++
weight = 96
title = "라빈-카프 (Rabin-Karp) 알고리즘"
date = "2024-03-21"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
1. **해시 기반 탐색**: 문자열을 수치화된 해시(Hash) 값으로 변환하여 매칭 여부를 빠르게 판단하는 [[001_algorithm_definition|알고리즘]]임.
2. **롤링 해시 (Rolling Hash)**: 이전 윈도우의 해시값을 활용하여 다음 윈도우의 해시를 $O(1)$에 계산하는 슬라이딩 윈도우 기법을 사용함.
3. **다중 패턴 탐색**: 하나의 텍스트에서 여러 개의 패턴을 동시에 찾을 때 특히 유리하며, 평균적으로 선형 [[002_time_complexity|시간 복잡도]]를 가짐.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
- **개념**: 1987년 Michael O. Rabin과 Richard M. Karp가 발표한 [[001_algorithm_definition|알고리즘]]으로, 단순 문자 비교 대신 지수 함수 기반의 [[195_polynomial_generator_crc|다항식]] 해시([[195_polynomial_generator_crc|Polynomial]] Rolling Hash)를 활용함.
- **필요성**: [[563_hash_collision_chaining_linear_probing|해시 충돌]](Hash [[563_hash_collision_chaining_linear_probing|Collision]])의 위험이 있으나, 적절한 소수(Prime)와 진법(Base) 선택으로 실무적 활용도를 높임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
#### 1. 롤링 해시의 매커니즘
- **윈도우 이동**: 다음 해시 = (진법 $\times$ (현재 해시 - 첫 글자 [[267_weight_bias_activation|가중치]]) + 새로운 글자) mod 소수.

```text
[ Rabin-Karp Rolling Hash Logic ]
Text:    H E L L O _ W O R L D
Pattern: L L O (Hash Value = P_Hash)

Step 1: Hash("HEL") != P_Hash (Skip)
Step 2: Hash("ELL") != P_Hash (Skip)
Step 3: Hash("LLO") == P_Hash (Potential Match!)

[ Hash Calculation Formula ]
H = (c1 * d^(m-1) + c2 * d^(m-2) + ... + cm * d^0) mod q
- d: Base (e.g., 256 for ASCII)
- q: Large Prime Number
- m: Pattern Length
```

#### 2. [[563_hash_collision_chaining_linear_probing|해시 충돌]] 방지
- 해시값이 일치하더라도 실제로 문자열이 같은지 한 번 더 [[396_validation|확인]]([[395_verification_process_review|Verification]])하여 정확성을 보장함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 라빈-카프 (Rabin-Karp) | [[094_kmp_algorithm|KMP]] [[001_algorithm_definition|알고리즘]] | [[095_boyer_moore_algorithm|보이어-무어]] ([[095_boyer_moore_algorithm|Boyer-Moore]]) |
| :--- | :--- | :--- | :--- |
| **핵심 원리** | 해시 값 비교 | 실패 함수 (LPS) | 스킵 테이블 (Bad Char/Good Suffix) |
| **[[002_time_complexity|시간 복잡도]]** | 평균 $O(N+M)$, 최악 $O(N \cdot M)$ | $O(N+M)$ | $O(N/M)$ |
| **주요 장점** | 다중 패턴 탐색 시 효율적 | 이론적 최악 [[282_performance_tactics|성능]] 보장 | 대부분의 실무 [[001_dikw_pyramid|데이터]]에서 최적 |
| **[[563_hash_collision_chaining_linear_probing|해시 충돌]]** | 발생 가능 ([[395_verification_process_review|검증]] 단계 필요) | 없음 | 없음 |
| **적용 분야** | 표절 검사, 침입 탐지 | 바이너리 탐색, DNA 분석 | 텍스트 검색 (Grep, 에디터) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
- **실무 적용**: 문서 표절 검출(두 문서의 해시 집합 비교), 고정된 시그니처가 많은 네트워크 [[601_ids_ips_syscall_tracing|침입 탐지 시스템]].
- **기술사적 판단**: 라빈-카프는 단일 패턴 검색에서는 [[095_boyer_moore_algorithm|보이어-무어]]에 밀리지만, **다중 패턴 동시 검색**이 필요한 보안 장비나 **문서 유사도 비교**에서 압도적인 가치를 지님. [[667_hash_function_integrity_one_way|해시 함수]] 설계 시 오버플로우와 모듈러 연산 최적화가 필수적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 복잡한 문자열 비교 문제를 수치 계산 문제로 전환하여 대규모 [[001_dikw_pyramid|데이터]] 집합의 유사성을 빠르게 정량화함.
- **결론**: [[001_algorithm_definition|알고리즘]]과 대수학의 융합을 보여주는 사례로, 현대 [[001_dikw_pyramid|데이터]] 마이닝과 보안 기술의 근간이 되는 [[001_algorithm_definition|알고리즘]]임.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: 문자열 탐색, [[667_hash_function_integrity_one_way|해시 함수]]
- **하위 개념**: Rolling Hash, Fingerprinting
- **융합 응용**: [[061_bloomfilter|Bloom Filter]] (공간 효율적 필터링)

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 문자열 탐색, 해시 함수]
    │
    ▼
[하위 개념: Rolling Hash, Fingerprinting]
    │
    ▼
[융합 응용: Bloom Filter (공간 효율적 필터링)]
```

이 흐름도는 상위 개념: 문자열 탐색, [[667_hash_function_integrity_one_way|해시 함수]]에서 출발해 융합 응용: [[061_bloomfilter|Bloom Filter]] (공간 효율적 필터링)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 가방 속에 숨긴 장난감 이름을 하나하나 [[396_validation|확인]]하는 대신, 가방의 "무게"를 먼저 재보는 것과 같아요.
2. 무게가 같으면 그제야 가방을 열어 진짜 장난감이 들어있는지 [[396_validation|확인]]하는 영리한 방법이죠.
3. 기차 칸을 하나씩 이동하며 무게를 잴 때, 내리는 사람 몸무게는 빼고 타는 사람 몸무게는 더하면 금방 계산되겠죠?
