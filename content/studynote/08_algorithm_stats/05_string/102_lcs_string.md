+++
title = "9. 최장 공통 부분수열 (LCS, Longest Common Subsequence) — 문자열 비교"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) ([Longest Common Subsequence](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/))는 두 문자열에서 순서를 유지하면서(연속일 필요 없음) 공통으로 존재하는 가장 긴 부분수열을 [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/))으로 O(mn)에 구하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: git diff의 두 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 비교, DNA 서열 정렬, 문서 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리의 변경 사항 추적이 모두 LCS를 기반으로 하며, 두 시퀀스의 공통 구조를 발견하는 범용 문제 해결 도구다.
> 3. **판단 포인트**: LCS는 부분수열(비연속 가능), [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) (Longest Common Substring)는 부분 문자열(연속 필수), [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)([Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/))는 변환 비용으로 세 개념을 명확히 구분하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

두 DNA 서열 "AGGTAB"과 "GXTXAYB"에서 공통 진화 코드를 찾거나, 두 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에서 공통 줄을 찾아 diff를 생성하는 문제가 LCS다. 순서를 유지하지만 연속일 필요가 없으므로 단순 부분 문자열 탐색과 다르다. 중복 부분 문제 구조(Optimal Substructure + Overlapping Subproblems)를 가지므로 DP가 최적 해법이다.

### 부분수열 vs 부분 문자열

```
문자열: "ABCDE"

부분수열 (Subsequence): 순서 유지, 연속 불필요
  "ACE", "BD", "ABCDE", "A", ""  ← 모두 유효

부분 문자열 (Substring): 순서 유지, 연속 필수
  "ABC", "BCD", "CDE"            ← 연속된 것만 유효
  "ACE"                           ← X (연속 아님)
```

📢 **섹션 요약 비유**: LCS는 두 악보에서 같은 음표들이 같은 순서로 나타나는 가장 긴 멜로디를 찾는 것—연속일 필요 없이 순서만 지키면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) DP 점화식

```
s1 = "ABCBDAB", s2 = "BDCAB"

dp[i][j] = s1[0..i-1]과 s2[0..j-1]의 LCS 길이

점화식:
  if s1[i-1] == s2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
  else:                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

DP 테이블:
       ""  B  D  C  A  B
   ""  [0, 0, 0, 0, 0, 0]
   A   [0, 0, 0, 0, 1, 1]
   B   [0, 1, 1, 1, 1, 2]
   C   [0, 1, 1, 2, 2, 2]
   B   [0, 1, 1, 2, 2, 3]
   D   [0, 1, 2, 2, 2, 3]
   A   [0, 1, 2, 2, 3, 3]
   B   [0, 1, 2, 2, 3, 4]

LCS 길이 = dp[7][5] = 4
```

### 역추적 ([Backtracking](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/))으로 [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) 복원

```
dp 테이블 역추적:
  dp[7][5]=4: s1[6]='B'==s2[4]='B' → 'B' 선택, dp[6][4]로 이동
  dp[6][4]=3: s1[5]='A'==s2[3]='A' → 'A' 선택, dp[5][3]으로 이동
  dp[5][3]=2: s1[4]='D'≠s2[2]='C' → max 방향(dp[4][3])으로 이동
  dp[4][3]=2: s1[3]='B'≠s2[2]='C' → max 방향(dp[3][3])으로 이동
  dp[3][3]=2: s1[2]='C'==s2[2]='C' → 'C' 선택, dp[2][2]로 이동
  dp[2][2]=1: s1[1]='B'==s2[1]='D'? 아니오, dp[1][2] 방향
  ...
  LCS = "BCAB" (4글자)
```

### 공간 최적화: O(min(m,n))

```
dp 테이블 전체 O(mn)이 불필요한 경우:
  LCS 길이만 필요 → 이전 행 하나만 유지 O(min(m,n))
  LCS 복원 필요   → 전체 테이블 O(mn) 또는 Hirschberg 알고리즘 O(mn) 시간 O(min(m,n)) 공간
```

📢 **섹션 요약 비유**: DP 테이블은 두 서열을 격자판 위에 놓고 공통 체크포인트를 이어가는 게임—각 칸은 "여기까지의 최선 공통 경로 길이"를 기억한다.

---

## Ⅲ. 비교 및 연결

### [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) vs [LIS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/) vs [Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)

| 항목 | [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) | [LIS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/) (최장 증가 부분수열) | [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/) |
|:---|:---|:---|:---|
| 입력 | 두 시퀀스 | 단일 시퀀스 | 두 문자열 |
| 목표 | 공통 부분수열 최장화 | 증가하는 부분수열 최장화 | 변환 최소 연산 수 |
| DP 시간 | O(mn) | O(n log n) | O(mn) |
| 주요 활용 | diff, DNA 정렬 | 인내심 게임, 주식 | 맞춤법, fuzzy 검색 |

### LCS와 [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

```
LCS 길이 = L, 두 문자열 길이 m, n이면:
  편집 거리 (삽입+삭제만) = m + n - 2L

"ABCD" vs "ACBD":
  LCS = "ACD" (L=3)
  편집 거리 = 4+4-6 = 2
```

### 실제 응용: git diff의 Myers [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

```
git diff는 LCS 기반 Myers 알고리즘 사용:
  두 파일 버전을 줄(line) 단위로 LCS 계산
  LCS에 없는 줄 → 삭제(-)
  상대방에만 있는 줄 → 추가(+)

예:
  파일1: [a, b, c, d]
  파일2: [a, c, e, d]
  LCS:   [a, c, d]
  diff:  - b (삭제), + e (추가)
```

📢 **섹션 요약 비유**: git diff는 두 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 책 두 권으로 보고, 공통 문장([LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/))을 기준으로 달라진 부분만 표시하는 거야—빨간 줄(삭제)과 초록 줄(추가)이 그 결과다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 (Version Control)**: git diff, SVN, Mercurial의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 비교 핵심
- **DNA 서열 정렬 (Sequence Alignment)**: 두 게놈의 공통 서열 분석 (Smith-Waterman, Needleman-Wunsch 변형)
- **표절 검사 (Plagiarism [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))**: 문서 간 공통 문장 구조 탐지
- **텍스트 편집기 Merge**: 3-way merge에서 공통 베이스와 두 분기 간 [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)
- **음악 유사도 분석**: 멜로디 시퀀스 비교

### 기술사 판단 기준

```
두 파일/서열 비교 + 공통 구조 추출      →  LCS O(mn)
두 문자열 변환 최소 비용                →  편집 거리 O(mn)
단일 시퀀스 증가 부분수열 최장화        →  LIS O(n log n)
연속 공통 부분 문자열                   →  LCS Substring 또는 서픽스 배열
빠른 LCS (큰 파일, 주로 동일)          →  Myers 알고리즘 O(nd)
```

📢 **섹션 요약 비유**: LCS는 두 음악가가 각자 연주한 악보에서 공통 악절을 찾는 작업—멀리 떨어진 음표도 순서만 같으면 공통으로 인정한다.

---

## Ⅴ. 기대효과 및 결론

LCS는 두 시퀀스의 공통 구조를 추출하는 핵심 DP [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, git diff·DNA 분석·표절 검사의 이론적 기반이다. O(mn) 시간과 공간은 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 부담이 되지만, Hirschberg [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 공간을 O(min(m,n))으로 줄이거나 Myers [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 편집 횟수(d)에 비례한 O(nd) 복잡도를 달성할 수 있다.

**결론**: 두 시퀀스의 유사도를 공통 구조 관점에서 분석해야 할 때 LCS가 표준 도구이며, [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)와의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이해하면 두 접근법을 상황에 맞게 선택할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/) ([Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)) | LCS와 수학적으로 연관된 문자열 유사도 |
| [LIS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/) ([Longest Increasing Subsequence](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/054_longest_increasing_subsequence/)) | 단일 시퀀스 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 DP 문제 |
| [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) ([Dynamic Programming](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)) | LCS의 핵심 해법 패러다임 |
| Myers [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | git diff의 [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) 최적화 변형 |
| 서픽스 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (Suffix [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)) | 연속 공통 부분 문자열 탐색 |
| Hirschberg [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | O(min(m,n)) 공간으로 [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) 복원 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[단순 비교(완전 탐색)]
    │
    ▼
[동적 프로그래밍(DP)]
    │
    ▼
[LCS 점화식]
    │
    ▼
[LCS 역추적]
    │
    ▼
[편집 거리(Edit Distance) 응용]
```

LCS는 부분수열 비교를 동적 계획법으로 풀며 역추적과 [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)로 확장된다.

### 👶 어린이를 위한 3줄 비유 설명

1. LCS는 두 친구가 각자 좋아하는 음식 목록에서 순서대로 겹치는 음식을 최대한 많이 찾는 거야.
2. "피자, 치킨, 떡볶이"와 "피자, 떡볶이, 치킨"에서 LCS는 "피자, 떡볶이" 또는 "피자, 치킨"이야.
3. git에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 어떻게 바뀌었는지 보여주는 것도 이 방법으로 공통 줄을 찾아서 달라진 부분만 표시해!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 102 / 175

← **이전**: [8. LZ77 / LZ78 / LZW — 사전 기반 압축](/knowledge-base/studynote/08_algorithm_stats/05_string/101_lz77_lz78_lzw/)
**다음**: [10. 편집 거리 (Edit Distance / Levenshtein Distance) — DP](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/) →

---
