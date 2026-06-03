+++
title = "10. 편집 거리 (Edit Distance / Levenshtein Distance) — DP"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 편집 거리 (Edit Distance, Levenshtein Distance)는 한 문자열을 다른 문자열로 변환하는 데 필요한 최소 삽입·삭제·대체 연산 수를 [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) (DP)으로 O(mn)에 계산하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 두 문자열이 "얼마나 다른가"를 정량화하므로, 맞춤법 교정·DNA [돌연변이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/638_mutation_testing_test_case_verification/) 분석·퍼지 검색(Fuzzy Search)·자동 완성에서 유사도 기반 판단의 표준 척도가 된다.
> 3. **판단 포인트**: 삽입·삭제·대체만 허용하면 Levenshtein, 전치(Transposition)도 허용하면 Damerau-Levenshtein Distance를 사용하며, 임계값 d 이하의 유사 문자열만 검색하면 BK-tree 또는 SymSpell로 최적화한다.

---

## Ⅰ. 개요 및 필요성

"kitten"을 "sitting"으로 바꾸려면 몇 번의 연산이 필요한가? 키보드 오타 교정, DNA 서열 변이 분석, 제품 이름 중복 탐지 모두 이 질문의 응용이다. 편집 거리는 이 최소 변환 비용을 정의하고 DP로 효율적으로 계산한다.

### 편집 연산 종류

| 연산 | 설명 | 예시 |
|:---|:---|:---|
| 삽입 (Insert) | 문자 추가 | "cat" → "cart" |
| 삭제 (Delete) | 문자 제거 | "cart" → "cat" |
| 대체 (Substitute) | 문자 교체 | "cat" → "bat" |
| 전치 (Transpose) | 인접 문자 교환 (DL only) | "ab" → "[ba](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)" |

📢 **섹션 요약 비유**: 편집 거리는 두 단어를 같은 단어로 만들기 위해 레고 블록을 추가·제거·교체하는 최소 횟수다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Levenshtein DP 테이블



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">s1 = "kitten", s2 = "sitting"</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= s1</div><div class="kb-diagram-node">0..i-1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">0..j-1</div><div class="kb-diagram-note">로 변환하는 최소 편집 수</div></div>
<div class="kb-diagram-note">점화식:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">if s1</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-note">== s2</div><div class="kb-diagram-node">j-1</div><div class="kb-diagram-note">: dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-node">j-1</div><div class="kb-diagram-note">(문자 일치)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">else: dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= 1 + min(</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-node">j</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">s1에서 삭제</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j-1</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">s2에 삽입</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-node">j-1</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">대체</div></div>
<div class="kb-diagram-note">)</div>
<div class="kb-diagram-note">DP 테이블:</div>
<div class="kb-diagram-note">"" s i t t i n g</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">""</div><div class="kb-diagram-node">0, 1, 2, 3, 4, 5, 6, 7</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">k</div><div class="kb-diagram-node">1, 1, 2, 3, 4, 5, 6, 7</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">i</div><div class="kb-diagram-node">2, 2, 1, 2, 3, 4, 5, 6</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">t</div><div class="kb-diagram-node">3, 3, 2, 1, 2, 3, 4, 5</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">t</div><div class="kb-diagram-node">4, 4, 3, 2, 1, 2, 3, 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">e</div><div class="kb-diagram-node">5, 5, 4, 3, 2, 2, 3, 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">n</div><div class="kb-diagram-node">6, 6, 5, 4, 3, 3, 2, 3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">편집 거리 = dp</div><div class="kb-diagram-node">6</div><div class="kb-diagram-node">7</div><div class="kb-diagram-note">= 3</div></div>
<div class="kb-diagram-note">(kitten → sitten → sittin → sitting)</div>
</div>
</div>



### 역추적: 연산 시퀀스 복원



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">6</div><div class="kb-diagram-node">7</div><div class="kb-diagram-note">=3:</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">s1</div><div class="kb-diagram-node">5</div><div class="kb-diagram-note">='n' ≠ s2</div><div class="kb-diagram-node">6</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">5</div><div class="kb-diagram-node">7</div><div class="kb-diagram-note">=4에서 대체(1)</div></div>
<div class="kb-diagram-note">역추적 경로:</div>
<div class="kb-diagram-note">(6,7)→(5,6)→(4,5)→(3,4)→(2,3)→(1,2)→(0,0)</div>
<div class="kb-diagram-note">연산:</div>
<div class="kb-diagram-note">k→s: 대체 (1)</div>
<div class="kb-diagram-note">e→i: 대체 (1)</div>
<div class="kb-diagram-note">_→g: 삽입 (1)</div>
<div class="kb-diagram-note">총 3회</div>
</div>
</div>



### 공간 최적화: O(min(m,n))

```
길이만 필요한 경우:
  i번째 행 계산에 (i-1)번째 행만 필요
  → 두 행만 유지: O(min(m,n)) 공간

prev_row = [0,1,2,...,n]
curr_row = [0, ...]
각 행 처리 후 swap
```

### Damerau-Levenshtein Distance



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전치 연산 추가:</div>
<div class="kb-diagram-note">"ab" → "ba": Levenshtein = 2 (ab→xb→ba), DL = 1 (전치 1회)</div>
<div class="kb-diagram-note">실제 오타의 ~80%는 단일 삽입·삭제·대체·전치로 설명 가능</div>
<div class="kb-diagram-note">→ 맞춤법 교정에는 DL Distance가 Levenshtein보다 정확</div>
</div>
</div>



📢 **섹션 요약 비유**: DP 테이블은 두 단어 사이의 변환 지도—오른쪽은 삽입, 아래는 삭제, 대각선은 대체·일치를 나타내며, 왼쪽 위에서 오른쪽 아래로 가는 최소 비용 경로가 편집 거리다.

---

## Ⅲ. 비교 및 연결

### 편집 거리 vs [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) vs 자카드 유사도

| 항목 | 편집 거리 | [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) | 자카드 유사도 |
|:---|:---|:---|:---|
| 측정 | 변환 비용 (낮을수록 유사) | 공통 길이 (높을수록 유사) | 집합 교집합/합집합 |
| 연산 | O(mn) | O(mn) | O(n+m) |
| 적합 | 맞춤법, 오타 | diff, DNA | 문서 유사도 |

### 임계값 기반 퍼지 검색 (Fuzzy Search)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SymSpell 알고리즘 (편집 거리 ≤ 2):</div>
<div class="kb-diagram-note">사전의 모든 단어와 그 편집 거리 ≤ 2 변형을 해시맵에 저장</div>
<div class="kb-diagram-note">쿼리 단어의 변형을 생성해 해시맵 조회</div>
<div class="kb-diagram-note">→ O(1) 평균 조회 (브루트포스 O(dictionary_size) 대비)</div>
<div class="kb-diagram-note">BK-tree:</div>
<div class="kb-diagram-note">편집 거리를 거리 함수로 사용한 트리 구조</div>
<div class="kb-diagram-note">query(q, threshold=2) → d(root, q) ± 2 범위 노드만 탐색</div>
<div class="kb-diagram-note">→ 대용량 사전에서 퍼지 검색 최적화</div>
</div>
</div>



📢 **섹션 요약 비유**: BK-tree는 도시 지도에서 "반경 2km 이내 식당"을 찾는 것처럼, 편집 거리를 반경으로 삼아 사전에서 유사 단어를 빠르게 검색한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **맞춤법 교정 (Spell Checker)**: MS [Word](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/), Google 검색의 "혹시 이 단어를 찾으셨나요?" — DL Distance 기반
- **DNA/단백질 서열 분석**: [돌연변이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/638_mutation_testing_test_case_verification/)(Mutation) 수 = 편집 거리 (Smith-Waterma 변형)
- **자동 완성 (Autocomplete)**: 오타 허용 검색, 편집 거리 ≤ 2인 단어 추천
- **레코드 링크 (Record Linkage)**: 데이터베이스에서 동일인물/기업명 중복 탐지
- **표절 탐지**: 일부 문자 변경 후 복사한 텍스트 탐지

### 기술사 판단 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">문자열 유사도 정량화 → 편집 거리 O(mn)</div>
<div class="kb-diagram-note">전치 오타 포함 교정 → Damerau-Levenshtein</div>
<div class="kb-diagram-note">대용량 사전 퍼지 검색 → SymSpell (O(1)) 또는 BK-tree</div>
<div class="kb-diagram-note">DNA 국소 정렬 (일부 서열 비교) → Smith-Waterman (편집 거리 변형)</div>
<div class="kb-diagram-note">DNA 전역 정렬 → Needleman-Wunsch</div>
<div class="kb-diagram-note">공통 구조 추출 → LCS (편집 거리 대신)</div>
</div>
</div>



📢 **섹션 요약 비유**: 편집 거리는 두 단어를 같은 단어로 만들기 위해 지불하는 "변환 요금"—거리가 작을수록 두 단어는 비슷하고, 맞춤법 교정 시스템은 요금이 가장 낮은 단어를 추천한다.

---

## Ⅴ. 기대효과 및 결론

편집 거리는 두 문자열의 유사도를 변환 비용으로 정량화하는 가장 직관적이고 범용적인 척도다. O(mn) DP로 정확하게 계산할 수 있으며, 실용적인 맞춤법 교정 시스템에서는 Damerau-Levenshtein과 SymSpell로 정확도와 속도를 동시에 높인다. DNA 분석에서는 가중치를 추가한 변형(Smith-Waterman)이 생물학적 의미에 맞게 확장된다.

**결론**: 오타·유사 문자열·변이 서열 분석에서 편집 거리는 표준 척도이며, DP를 넘어 BK-tree/SymSpell로의 최적화가 실무 시스템의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) ([Longest Common Subsequence](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/)) | 관련 DP, 편집 거리 = m+n-2×[LCS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/053_lcs/) |
| Damerau-Levenshtein | 전치 연산 추가 확장 |
| BK-tree | 편집 거리 기반 퍼지 검색 트리 |
| SymSpell | O(1) 퍼지 검색 사전 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| Smith-Waterman | DNA 국소 정렬 편집 거리 변형 |
| [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) (DP) | 편집 거리의 핵심 풀이 패러다임 |

---

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">문자열 비교 (String Comparison) — 차이 정량화 필요</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">동적 프로그래밍 (DP) — 최소 변환 비용 테이블</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">레벤슈타인 거리 (Levenshtein Distance) — 삽입·삭제·대체</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다메라우-레벤슈타인 거리 (Damerau-Levenshtein Distance) — 전치 포함</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">퍼지 검색 / 맞춤법 교정 — 유사 문자열 실무 적용</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시퀀스 정렬 / BK-tree / SymSpell — 대규모 검색 최적화</div></div>
</div>
</div>


편집 거리는 DP로 최소 변환 비용을 계산하는 문자열 유사도의 표준이며, 퍼지 검색과 맞춤법 교정의 기반으로 확장되었다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편집 거리는 단어 퍼즐 게임이야—"kitten"을 "sitting"으로 바꿀 때 몇 번 글자를 바꾸거나 추가·삭제해야 하는지 세는 거야.
2. 표 형태로 천천히 채워나가면 가장 적게 바꾸는 방법을 자동으로 찾을 수 있어—이게 바로 DP야.
3. 맞춤법 교정 프로그램이 "혹시 이 단어?" 라고 제안하는 건, 편집 거리가 1~2인 단어들을 찾아서 보여주는 것이야!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 103 / 175

← **이전**: [9. 최장 공통 부분수열 (LCS, Longest Common Subsequence) — 문자열 비교](/knowledge-base/studynote/08_algorithm_stats/05_string/102_lcs_string/)
**다음**: [11. 정규 표현식 (Regex, Regular Expression) — NFA/DFA, 패턴 매칭](/knowledge-base/studynote/08_algorithm_stats/05_string/104_regex/) →

---
