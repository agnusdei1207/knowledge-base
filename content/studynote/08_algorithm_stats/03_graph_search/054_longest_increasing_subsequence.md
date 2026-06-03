+++
title = "24. LIS (Longest Increasing Subsequence) — 최장 증가 부분 수열"
date = 2026-04-29

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LIS (Longest Increasing Subsequence, 최장 증가 부분 수열)는 주어진 수열에서 값이 오름차순으로 증가하는 원소들의 가장 긴 부분 수열을 찾는 문제로, [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)(DP) O(n²) 또는 [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) 기반 O(n log n) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 해결된다.
> 2. **가치**: LIS는 단독 문제보다 다른 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 서브루틴으로 등장하는 경우가 많다 — [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)([Longest Common Subsequence](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/))·[편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)([Edit Distance](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/))와 유사한 DP 구조를 공유하며, 인내 정렬(Patience Sorting)과 연계하여 O(n log n) 최적 구현이 가능하다.
> 3. **판단 포인트**: O(n²) DP는 LIS 복원(역추적, [Backtracking](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/))이 쉬운 반면, O(n log n) [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)은 복원이 추가 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 없이는 불가능하다. 길이만 필요하면 O(n log n), 실제 수열 복원이 필요하면 O(n²) DP 또는 별도 parent [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

수열 A = [3, 1, 4, 1, 5, 9, 2, 6]에서 LIS를 구하면 [1, 4, 5, 9] 또는 [1, 4, 5, 6] (길이 4)가 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">LIS 시각화: A =</div><div class="kb-diagram-node">3, 1, 4, 1, 5, 9, 2, 6</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인덱스: 0 1 2 3 4 5 6 7</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">값: 3 1 4 1 5 9 2 6</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">: 1 1 2 1 3 4 2 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= A</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">로 끝나는 LIS 길이</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">4</div><div class="kb-diagram-note">=3: A</div><div class="kb-diagram-node">1</div><div class="kb-diagram-note">=1 &lt; A</div><div class="kb-diagram-node">2</div><div class="kb-diagram-note">=4 &lt; A</div><div class="kb-diagram-node">4</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">길이 3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">길이 4</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">max(dp) = 4 → LIS 길이 = 4</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: LIS는 계단 오르기다. 주어진 숫자들 중에서 뒤로 내려가지 않고 계속 올라가는 가장 긴 경로를 찾는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### O(n²) DP 구현

```python
def lis_dp(arr):
    n = len(arr)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

### O(n log n) 인내 정렬 (Patience Sorting) 기반

```python
import bisect

def lis_nlogn(arr):
    tails = []          # tails[i]: 길이 i+1인 IS의 최솟값
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x   # 더 작은 값으로 교체 → 미래 확장 가능성 ↑
    return len(tails)
```

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | 공간 | 수열 복원 |
|:---|:---:|:---:|:---:|
| DP (O(n²)) | O(n²) | O(n) | 쉬움 (parent [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)) |
| [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) (O(n log n)) | O(n log n) | O(n) | 추가 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 필요 |

- **📢 섹션 요약 비유**: O(n log n)은 카드를 인내 게임(Patience Game)처럼 최소한의 더미로 쌓는 방식이다. 각 더미의 맨 위 카드가 tails [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이며, 새 카드가 들어갈 더미를 [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/)으로 찾는다.

---

## Ⅲ. 비교 및 연결

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/">LCS</a> (최장 공통 부분 수열)</strong> | LIS의 DP 구조와 유사; 2D DP |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/">편집 거리</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/">Edit Distance</a>)</strong> | DP 테이블 구조 동일한 패밀리 |
| **인내 정렬** | O(n log n) LIS의 직관적 이해 도구 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/">이진 탐색</a> (bisect)</strong> | tails [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 갱신의 핵심 연산 |

- **📢 섹션 요약 비유**: LIS, [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/), [편집 거리](/knowledge-base/studynote/08_algorithm_stats/05_string/103_edit_distance/)는 모두 같은 DP 가족이다. 부분 문제의 답을 테이블에 저장하고 재사용하는 핵심 원리를 공유하며, LIS를 이해하면 나머지도 자연스럽게 이해된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 의존성 체인 분석
n개의 소프트웨어 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 번호 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 역방향 호환을 유지하는 최장 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 체인 길이 계산.

- [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 번호를 정수로 변환 후 LIS O(n log n) 적용.
- 결과: 최장 호환 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 체인 길이 → 업그레이드 경로 최적화.

### 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 문제
- BOJ 11053 (LIS, O(n²))
- BOJ 12015 (LIS O(n log n))
- BOJ 14002 (LIS 복원)
- LeetCode 300 (Longest Increasing Subsequence)

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- n=100,000 이상의 입력에 O(n²) DP를 적용하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). n=100,000이면 10¹⁰ 연산으로 시간 초과가 발생한다. 길이가 크면 반드시 O(n log n) [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) 접근을 사용해야 한다.

- **📢 섹션 요약 비유**: 10만 명의 학생 키를 O(n²)로 처리하는 건 모든 학생 쌍을 직접 비교하는 것이다. O(n log n)은 이미 줄 세워진 학생 중 자신이 들어갈 자리를 빠르게 찾는 것이다.

---

## Ⅴ. 기대효과 및 결론

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 최대 n | 적용 상황 |
|:---|:---:|:---|
| DP O(n²) | ~5,000 | 복원 필요, 이해 우선 |
| [이진 탐색](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) O(n log n) | ~100,000+ | 길이만 필요, 대용량 |

LIS [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 인내 정렬(Patience Sorting) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 수학적 기반이기도 하며, 카드 게임 이론과의 흥미로운 연결점을 가진다. 딜워스 정리(Dilworth's Theorem)에 의해 LIS 길이는 감소 부분 수열로 분할하는 최소 수와 같다는 이원 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도 흥미롭다.

- **📢 섹션 요약 비유**: LIS는 인생의 상승 구간 찾기다. 주어진 경험(수열) 중에서 계속 성장하는(증가하는) 경험의 가장 긴 흐름을 찾아내는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 속에서 최선의 오름세를 찾아낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/">동적 프로그래밍</a> (DP)</strong> | LIS O(n²)의 핵심 기법 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/">이진 탐색</a></strong> | O(n log n) LIS에서 tails [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 갱신 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/">LCS</a></strong> | 유사한 DP 구조; 2개 수열 비교 |
| **인내 정렬** | O(n log n) LIS의 직관적 카드 게임 모델 |
| **딜워스 정리** | LIS와 감소 수열 분할의 이원 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">기초 DP — 부분 문제 최적해 저장, O(n²) LIS</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">인내 정렬 모델 — 카드 더미, tails 배열 직관</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이진 탐색 최적화 — O(n log n) LIS</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LCS / 편집 거리 — LIS DP 패밀리 확장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">딜워스 정리 — LIS의 이론적 이원 대응</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. LIS는 계단처럼 계속 올라가는 숫자들의 가장 긴 줄을 찾는 퍼즐이에요!
2. 예를 들어 [3, 1, 4, 1, 5, 9, 2, 6]에서 1→4→5→9처럼 계속 커지는 숫자 4개를 찾는 거예요.
3. 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 컴퓨터가 가장 긴 성장 패턴을 빠르게 찾을 때 사용된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 175

← **이전**: [23. LCS (Longest Common Subsequence) — 최장 공통 부분 수열](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)
**다음**: [1. 배열 (Array) — 연속 메모리, O(1) 랜덤 접근](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) →

---
