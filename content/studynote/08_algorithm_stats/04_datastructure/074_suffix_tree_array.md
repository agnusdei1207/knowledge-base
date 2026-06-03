---
title: 22. 서픽스 트리/배열 (Suffix Tree/Array) — 문자열 분석
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서픽스 트리 (Suffix Tree)와 서픽스 [[055_array|배열]] (Suffix [[055_array|Array]])은 문자열의 모든 접미사(Suffix)를 인덱싱하여 부분 문자열 탐색·최장 반복 부분 문자열 등을 선형 시간에 처리하는 고급 문자열 자료구조다.
> 2. **가치**: 서픽스 [[055_array|배열]]은 서픽스 트리의 공간을 1/[[489_raid_10_hybrid|10]] 이하로 줄이면서 동등한 [[298_qkv_attention|쿼리]] 성능을 제공하므로, DNA 분석·텍스트 [[347_compaction|압축]]·검색 엔진에서 실질적으로 광범위하게 활용된다.
> 3. **판단 포인트**: 메모리가 충분하고 구현 복잡도를 감수할 수 있으면 서픽스 트리, 공간 절약과 캐시 효율이 중요하면 서픽스 [[055_array|배열]] + [[225_lcp_link_control_protocol|LCP]] (Longest Common Prefix) [[055_array|배열]]을 선택한다.

---

## Ⅰ. 개요 및 필요성

문자열 "banana"의 부분 문자열이 존재하는지를 단순 탐색(O(n×m))으로는 긴 텍스트에서 너무 느리다. 서픽스 트리는 텍스트의 모든 접미사를 [[087_trie|트라이]]([[066_trie|Trie]])로 [[347_compaction|압축]] 저장하여 임의 패턴을 O(m) 시간에 탐색한다. 단, 메모리 사용이 크므로 실용 시스템은 서픽스 [[055_array|배열]]로 대체한다.

### 접미사 목록 (문자열 "banana$")

| [[154_database_index_b_tree_search_optimization|인덱스]] | 접미사 |
|:---:|:---|
| 0 | banana$ |
| 1 | anana$ |
| 2 | nana$ |
| 3 | ana$ |
| 4 | na$ |
| 5 | a$ |
| 6 | $ |

`$`는 사전식 최소 종료 기호

📢 **섹션 요약 비유**: 서픽스 [[055_array|배열]]은 책의 모든 단어로 시작하는 "뒤집힌 색인"—"ana"를 찾으려면 이미 정렬된 색인에서 이진 탐색으로 바로 찾는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 서픽스 [[055_array|배열]] 구성

```
문자열: "banana$"
모든 접미사를 사전순 정렬:

SA (Suffix Array)   LCP Array
 6  "$"              -
 5  "a$"             0
 3  "ana$"           1   ← "a$"와 LCP=1 ("a")
 1  "anana$"         3   ← "ana$"와 LCP=3 ("ana")
 0  "banana$"        0
 4  "na$"            0
 2  "nana$"          2   ← "na$"와 LCP=2 ("na")

SA = [6, 5, 3, 1, 0, 4, 2]
LCP = [-, 0, 1, 3, 0, 0, 2]
```

### 서픽스 [[055_array|배열]] 기반 패턴 탐색

```
패턴 "ana" 탐색:
  SA의 정렬된 접미사에서 이진 탐색
  "ana" ≤ SA[2]="ana$" ← lower bound
  "ana" < SA[4]="banana$" ← upper bound
  → SA[2], SA[3] 두 위치에서 발생 (인덱스 3, 1)

시간: O(m log n), LCP 활용 시 O(m + log n)
```

### [[225_lcp_link_control_protocol|LCP]] (Longest Common Prefix) [[055_array|배열]] 활용

[[225_lcp_link_control_protocol|LCP]] [[055_array|배열]]은 인접한 두 접미사 간의 가장 긴 공통 접두사 길이를 저장한다.

- **최장 반복 부분 문자열**: [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]]의 최댓값 위치 = 가장 긴 반복 패턴
- **구간 [[298_qkv_attention|쿼리]] (RMQ)**: [[225_lcp_link_control_protocol|LCP]][i..j]의 최솟값 = [[767_sa_standalone_5g_core_network|SA]][i]와 [[767_sa_standalone_5g_core_network|SA]][j] 접미사의 [[225_lcp_link_control_protocol|LCP]]

```
LCP 최댓값 = 3 (인덱스 3, "anana$"와 "ana$"의 공통 "ana")
→ 문자열 "banana"에서 가장 긴 반복 부분 문자열은 "ana"
```

### 서픽스 트리 vs 서픽스 [[055_array|배열]]

| 항목 | 서픽스 트리 | 서픽스 [[055_array|배열]] |
|:---|:---:|:---:|
| 공간 | O(n) 상수 큼 (~20n [[074_byte|바이트]]) | O(n) 상수 작음 (~4n [[074_byte|바이트]]) |
| 구성 시간 | O(n) Ukkonen [[001_algorithm_definition|알고리즘]] | O(n log n) 또는 O(n) [[767_sa_standalone_5g_core_network|SA]]-IS |
| 패턴 탐색 | O(m) | O(m log n) |
| 구현 복잡도 | 높음 | 중간 |
| 캐시 효율 | 낮음 (포인터 트리) | 높음 (연속 [[055_array|배열]]) |

📢 **섹션 요약 비유**: 서픽스 트리는 대형 도서관의 정교한 카드 목록, 서픽스 [[055_array|배열]]은 같은 내용을 종이 한 장에 [[347_compaction|압축]]한 색인표—후자가 들고 다니기 훨씬 편하다.

---

## Ⅲ. 비교 및 연결

### 서픽스 트리 구조 ([[347_compaction|압축]] [[087_trie|트라이]])

```
"banana$"의 서픽스 트리 (일부):

        (root)
       /    \    \
     a        b    n
     |        |    |
    na        a    a
   / \        n    n
  na  $       a    a
  |   |       $    $
  $   (leaf)
```

[[347_compaction|압축]] [[087_trie|트라이]]([[073_compressed_trie|Compressed Trie]]): 단일 자식 체인을 하나의 레이블로 합쳐 노드 수를 O(n)으로 제한.

### 서픽스 [[055_array|배열]]과 다른 자료구조 비교

| 문제 | 자료구조 | 시간 |
|:---|:---:|:---:|
| 단순 패턴 탐색 ([[094_kmp_algorithm|KMP]]) | 실패 함수 [[055_array|배열]] | O(n+m) |
| 다중 패턴 탐색 | [[098_aho_corasick|Aho-Corasick]] | O(n+m+z) |
| 접두사 [[298_qkv_attention|쿼리]] | [[087_trie|트라이]] ([[066_trie|Trie]]) | O(m) |
| 임의 부분 문자열 | 서픽스 [[055_array|배열]] | O(m log n) |
| 최장 공통 부분 문자열 | 서픽스 [[055_array|배열]]+[[225_lcp_link_control_protocol|LCP]] | O(n) |
| 문자열 [[347_compaction|압축]] | [[767_sa_standalone_5g_core_network|SA]] + BWT | O(n) |

📢 **섹션 요약 비유**: 서픽스 [[055_array|배열]]은 문자열 분석의 만능 열쇠—한 번 만들어두면 부분 문자열 탐색, 반복 패턴 발견, [[347_compaction|압축]]까지 여러 용도로 쓸 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **DNA 분석**: 게놈 서열에서 반복 패턴, 서열 정렬 (BWA, Bowtie 등)
- **전문 검색 엔진**: 역인덱스 구축, 와일드카드 검색
- **[[159_compression|데이터 압축]]**: BWT (Burrows-Wheeler Transform) = 서픽스 [[055_array|배열]] 기반 → bzip2, 롤링 [[347_compaction|압축]]
- **표절 검사**: 긴 공통 부분 문자열 탐지
- **[[002_database_definition|데이터베이스]] 전문 검색**: PostgreSQL의 pg_trgm, [[302_cdc|Elasticsearch]] 역인덱스

### 기술사 판단 기준

```
짧은 패턴 1회 탐색               →  KMP O(n+m)
고정 패턴 집합 다중 탐색         →  Aho-Corasick
접두사 기반 자동 완성             →  압축 트라이
임의 부분 문자열 다중 쿼리       →  서픽스 배열 + LCP
DNA/전문 검색, 압축              →  서픽스 배열 + BWT
메모리 무제한 + 최고 탐색 속도  →  서픽스 트리
```

📢 **섹션 요약 비유**: 서픽스 [[055_array|배열]] 구축은 책의 모든 페이지를 찢어 알파벳 순으로 파일링하는 것—처음 한 번만 고생하면 이후 어떤 단어도 순식간에 찾는다.

---

## Ⅴ. 기대효과 및 결론

서픽스 [[055_array|배열]]은 서픽스 트리의 기능을 유지하면서 공간을 대폭 절감하여 실용적인 대안이 되었다. [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]]과 결합하면 최장 공통 부분 문자열, 최장 반복 부분 문자열, 구간 [[298_qkv_attention|쿼리]]를 선형 또는 O(m log n)에 처리할 수 있다. BWT와의 결합은 게놈 서열 분석과 [[347_compaction|압축]]의 핵심 기반이다.

**결론**: 문자열 집중 분석 시스템(DNA, 검색 엔진, [[159_compression|데이터 압축]])의 핵심 자료구조이며, 공간 효율이 중요한 실무에서는 서픽스 [[055_array|배열]]이 서픽스 트리를 대체한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] |
|:---|:---|
| [[087_trie|트라이]] ([[066_trie|Trie]]) | 서픽스 트리의 [[347_compaction|압축]] 전 기반 구조 |
| [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]] | 서픽스 [[055_array|배열]]의 보조 [[154_database_index_b_tree_search_optimization|인덱스]] |
| [[094_kmp_algorithm|KMP]] [[001_algorithm_definition|알고리즘]] | 단일 패턴 탐색의 O(n+m) 방법 |
| BWT (Burrows-Wheeler Transform) | 서픽스 [[055_array|배열]] 기반 [[347_compaction|압축]] 변환 |
| RMQ (Range Minimum Query) | [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]]의 구간 최솟값 [[298_qkv_attention|쿼리]] |
| [[347_compaction|압축]] [[087_trie|트라이]] ([[073_compressed_trie|Compressed Trie]]) | 서픽스 트리의 공간 최적화 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[전체 부분 문자열 (Substring) 인덱싱 필요]
    │
    ▼
[서픽스 트리 (Suffix Tree) — O(n) 구축, 높은 공간 비용]
    │
    ▼
[서픽스 배열 (Suffix Array) — 공간 효율 정렬 인덱스]
    │
    ▼
[LCP 배열 (Longest Common Prefix) — 반복 패턴 탐지]
    │
    ▼
[BWT (Burrows-Wheeler Transform) — 압축·검색 융합]
```
전체 부분 문자열 탐색을 위해 서픽스 트리를 고안하고, 공간 효율을 위해 서픽스 [[055_array|배열]]로 [[347_compaction|압축]]하며, [[225_lcp_link_control_protocol|LCP]] [[055_array|배열]]과 BWT로 DNA·검색엔진·[[347_compaction|압축]] [[001_algorithm_definition|알고리즘]]에 융합되는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 서픽스 [[055_array|배열]]은 책에 있는 모든 단어를 가나다 순으로 정리한 색인이야—"바나나"에서 시작하는 모든 끝부분을 정렬해두는 거야.
2. 원하는 단어를 찾을 때 처음부터 찾지 않고 이진 탐색으로 딱 중간부터 비교해서 빠르게 찾아.
3. LCP는 옆에 있는 두 색인 단어가 얼마나 공통 부분을 가지는지 기록해둔 표—반복 패턴을 찾는 데 쓰여.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 175

← **이전**: [[073_compressed_trie|압축된 트라이 (Compressed Trie / Patricia Trie)]]
**다음**: [[075_hashmap_vs_treemap|23. HashMap vs TreeMap — 해시맵과 트리맵 비교]] →

---
