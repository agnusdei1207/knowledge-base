+++
title = "008. 클리크 문제 — Clique Problem"
date = 2026-04-05

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

> **핵심 인사이트**
> 1. 클리크(Clique)란 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 모든 정점이 서로 연결된 완전 부분 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(Complete Subgraph)를 말하며 — k-Clique 문제(크기 k 이상의 클리크가 존재하는가?)는 SAT로부터 다항 시간 귀납에 의해 NP-완전임이 증명된다.
> 2. 클리크 문제는 사회 네트워크 분석(SNS에서 완전 연결 그룹 탐지), 생물정보학(단백질 상호작용 네트워크 분석), [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)(밀집 연결 사용자 클러스터 발견)에서 핵심 도구이지만 — 정확한 최대 클리크 탐색은 지수 시간이 소요된다.
> 3. 클리크(모든 쌍 연결)와 독립 집합(어떤 쌍도 연결 안 됨)은 여그래프(Complement [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))를 통해 동치로 환원되며 — 두 문제 모두 NP-완전이므로, 실용적으로는 근사 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 Bron-Kerbosch [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([백트래킹](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/) 기반)이 사용된다.

---

## Ⅰ. 클리크 정의



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클리크 (Clique):</div>
<div class="kb-diagram-note">그래프 G = (V, E)에서</div>
<div class="kb-diagram-note">클리크 C ⊆ V는:</div>
<div class="kb-diagram-note">C의 모든 두 정점 u, v에 대해 (u, v) ∈ E</div>
<div class="kb-diagram-note">즉, C 내부의 모든 쌍이 연결된 완전 부분 그래프</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">그래프:</div>
<div class="kb-diagram-note">1 - 2 - 3</div>
<div class="kb-diagram-note">4 - 5</div>
<div class="kb-diagram-note">클리크 {1,2,4}: 1-2, 2-4, 1-4 모두 연결? 1-4 없음 → Not clique</div>
<div class="kb-diagram-note">클리크 {1,2}: 1-2 연결 → size-2 clique ✓</div>
<div class="kb-diagram-note">클리크 {2,3}: 2-3 연결 → size-2 clique ✓</div>
<div class="kb-diagram-note">최대 클리크 (Maximum Clique):</div>
<div class="kb-diagram-note">그래프에서 가장 큰 클리크</div>
<div class="kb-diagram-note">크기를 ω(G)라 표기</div>
<div class="kb-diagram-note">k-클리크 결정 문제 (k-Clique Decision Problem):</div>
<div class="kb-diagram-note">"그래프 G에 크기 k 이상의 클리크가 존재하는가?"</div>
<div class="kb-diagram-note">→ NP-완전</div>
<div class="kb-diagram-note">클리크 최적화 문제:</div>
<div class="kb-diagram-note">"최대 클리크의 크기는?"</div>
<div class="kb-diagram-note">→ NP-하드</div>
<div class="kb-diagram-note">사회 네트워크 직관:</div>
<div class="kb-diagram-note">정점 = 사람</div>
<div class="kb-diagram-note">엣지 = 서로 아는 관계</div>
<div class="kb-diagram-note">클리크 = 모두가 서로 아는 그룹 (완전 연결 사교 그룹)</div>
<div class="kb-diagram-note">SNS 예: 3명이 모두 서로 팔로우 = size-3 클리크</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 클리크는 "모두가 서로 아는 친구 그룹" — 4명이 클리크이려면 4명 모두가 서로서로 친구여야 해요. 단 한 쌍이라도 모르면 클리크가 아니에요.

---

## Ⅱ. NP-완전 증명



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">k-클리크 ∈ NP 증명:</div>
<div class="kb-diagram-note">검증 (Verification):</div>
<div class="kb-diagram-note">주어진 부분 집합 C가 크기 k 클리크인지 확인</div>
<div class="kb-diagram-note">모든 쌍 (u,v) ∈ C에 대해 엣지 존재 확인</div>
<div class="kb-diagram-note">O(k^2) = O(n^2) → 다항 시간 검증 가능</div>
<div class="kb-diagram-note">→ k-Clique ∈ NP ✓</div>
<div class="kb-diagram-note">3-SAT ≤p k-Clique (3-SAT → k-Clique 다항 변환):</div>
<div class="kb-diagram-note">3-SAT 입력:</div>
<div class="kb-diagram-note">k개의 절 C1, ..., Ck</div>
<div class="kb-diagram-note">각 절 Ci = (xi1 ∨ xi2 ∨ xi3)</div>
<div class="kb-diagram-note">k-Clique 변환:</div>
<div class="kb-diagram-note">각 절의 각 리터럴 → 정점 생성</div>
<div class="kb-diagram-note">총 3k개의 정점</div>
<div class="kb-diagram-note">엣지 추가 규칙:</div>
<div class="kb-diagram-note">1. 같은 절의 리터럴 끼리는 연결 안 함</div>
<div class="kb-diagram-note">2. 다른 절의 리터럴 사이 연결:</div>
<div class="kb-diagram-note">모순이 아닐 때만 (xi와 ¬xi는 연결 안 함)</div>
<div class="kb-diagram-note">핵심 아이디어:</div>
<div class="kb-diagram-note">3-SAT가 만족 가능 ↔ 크기 k 클리크 존재</div>
<div class="kb-diagram-note">각 절에서 하나씩 리터럴을 선택 (k개 선택)</div>
<div class="kb-diagram-note">→ 선택한 k개가 모두 모순 없이 연결 = k-클리크</div>
<div class="kb-diagram-note">변환: O(n^2) → 다항 시간</div>
<div class="kb-diagram-note">따라서 3-SAT ≤p k-Clique</div>
<div class="kb-diagram-note">3-SAT는 NP-완전 + k-Clique ∈ NP</div>
<div class="kb-diagram-note">→ k-Clique는 NP-완전 ✓</div>
<div class="kb-diagram-note">클리크 ≡ 독립 집합 (Independent Set):</div>
<div class="kb-diagram-note">독립 집합 (Independent Set):</div>
<div class="kb-diagram-note">S ⊆ V에서 어떤 두 정점도 연결되지 않음</div>
<div class="kb-diagram-note">관계:</div>
<div class="kb-diagram-note">G의 여그래프 G-bar:</div>
<div class="kb-diagram-note">G의 엣지가 없는 곳 → G-bar에 엣지</div>
<div class="kb-diagram-note">G에서 클리크 C ↔ G-bar에서 독립 집합 C</div>
<div class="kb-diagram-note">→ Clique ≤p Independent Set (동치)</div>
<div class="kb-diagram-note">→ 둘 다 NP-완전</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 클리크 NP-완전 증명은 어려움의 연쇄 — SAT가 어렵다는 걸 알았고, SAT를 클리크 문제로 변환할 수 있으니 클리크도 어렵다! 어려움이 바이러스처럼 전파돼요.

---

## Ⅲ. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클리크 알고리즘:</div>
<div class="kb-diagram-note">1. 브루트 포스 (Brute Force):</div>
<div class="kb-diagram-note">모든 2^n 부분 집합 검사</div>
<div class="kb-diagram-note">각 부분 집합이 클리크인지 O(n^2) 검사</div>
<div class="kb-diagram-note">총: O(2^n × n^2)</div>
<div class="kb-diagram-note">n=50 → 2^50 ≈ 10^15 연산 → 실용 불가</div>
<div class="kb-diagram-note">2. Bron-Kerbosch 알고리즘 (1973):</div>
<div class="kb-diagram-note">백트래킹 기반 최대 클리크 탐색</div>
<div class="kb-diagram-note">BronKerbosch(R, P, X):</div>
<div class="kb-diagram-note">if P is empty and X is empty:</div>
<div class="kb-diagram-note">R은 극대 클리크 (Maximal Clique) 출력</div>
<div class="kb-diagram-note">for each vertex v in P:</div>
<div class="kb-diagram-note">BronKerbosch(R ∪ {v}, P ∩ N(v), X ∩ N(v))</div>
<div class="kb-diagram-note">P = P \ {v}</div>
<div class="kb-diagram-note">X = X ∪ {v}</div>
<div class="kb-diagram-note">피벗팅(Pivoting) 최적화:</div>
<div class="kb-diagram-note">가지치기로 실용적 속도 향상</div>
<div class="kb-diagram-note">희소 그래프에서 매우 빠름</div>
<div class="kb-diagram-note">3. 근사 알고리즘:</div>
<div class="kb-diagram-note">최대 클리크는 근사 어렵기로 유명</div>
<div class="kb-diagram-note">poly-log 근사비율도 NP-하드임이 증명됨 (Hastad, 1999)</div>
<div class="kb-diagram-note">실용: 휴리스틱 (유전 알고리즘, 시뮬레이티드 어닐링)</div>
<div class="kb-diagram-note">4. 파라미터화 알고리즘 (FPT):</div>
<div class="kb-diagram-note">k-클리크 문제:</div>
<div class="kb-diagram-note">O(2^k × n^ω) (ω: 행렬 곱셈 지수 ≈ 2.37)</div>
<div class="kb-diagram-note">k가 작으면 (k ≤ 20) 실용적</div>
<div class="kb-diagram-note">SNS 클리크 탐색 현실:</div>
<div class="kb-diagram-note">Facebook, Twitter: 수십억 노드</div>
<div class="kb-diagram-note">최대 클리크 탐색: 불가능 → 근사 사용</div>
<div class="kb-diagram-note">Dense Subgraph Discovery: 완화된 클리크 개념</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 클리크 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 퍼즐 최적화 — 모든 조합을 다 시도하는 건 너무 느리니, Bron-Kerbosch는 "이 방향은 어차피 안 될 것 같아" 하며 빠르게 [가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/).

---

## Ⅳ. 실용 응용

```
클리크 탐색 실용 응용:

1. 사회 네트워크 분석 (SNS):
   목적: 완전 연결 그룹 (친목 그룹) 탐지
   예: LinkedIn에서 모든 구성원이 서로 연결된 팀
   응용: 영향력자 식별, 광고 타겟팅
   
   실제: 완화된 개념 사용
   - 준-클리크 (quasi-clique): 80% 이상 연결
   - k-core: 각 정점이 최소 k개 이웃

2. 생물정보학 (Bioinformatics):
   단백질 상호작용 네트워크 (PPI Network):
   정점 = 단백질
   엣지 = 상호작용
   클리크 = 단백질 복합체 후보
   
   응용: 새로운 단백질 기능 예측
   질병 관련 단백질 클러스터 발견

3. 추천 시스템:
   사용자-아이템 이분 그래프에서 클리크
   = 동일 취향의 완전 사용자 그룹
   협업 필터링 초기 클러스터링

4. 컴파일러 최적화:
   레지스터 할당: 클리크 = 충돌 집합
   k-클리크 탐색 = 최소 레지스터 필요 개수

5. 패턴 인식:
   이미지 특징 매칭
   두 이미지의 특징점 → 클리크 = 매칭 그룹

MaxClique 벤치마크:
  DIMACS 그래프: 표준 클리크 테스트셋
  최고 성능 솔버: 수백 노드에서 최적해 탐색
  실용 한계: ~수천 노드
```

> 📢 **섹션 요약 비유**: 클리크 응용은 완전 연결 집단 탐지 — SNS에서 "이 5명은 서로 다 알아요"를 찾고, 생물학에서 "이 단백질들은 항상 같이 일해요"를 발견.

---

## Ⅴ. 실무 시나리오 — 생물정보학 단백질 복합체 탐지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단백질 상호작용 클리크 탐색:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">질병 연구에서 단백질 복합체 식별이 핵심</div>
<div class="kb-diagram-note">예: SARS-CoV-2 스파이크 단백질 상호작용 네트워크</div>
<div class="kb-diagram-note">입력 데이터:</div>
<div class="kb-diagram-note">BioGRID, STRING DB에서 PPI 데이터 다운로드</div>
<div class="kb-diagram-note">정점: 2만~3만 단백질</div>
<div class="kb-diagram-note">엣지: 수십만~수백만 상호작용</div>
<div class="kb-diagram-note">클리크 탐색 과정:</div>
<div class="kb-diagram-note">1. 네트워크 구성:</div>
<div class="kb-diagram-note">G = (단백질, 상호작용)</div>
<div class="kb-diagram-note">2. 필터링:</div>
<div class="kb-diagram-note">고신뢰도 상호작용만 유지 (confidence &gt; 0.7)</div>
<div class="kb-diagram-note">네트워크 밀도 감소 → Bron-Kerbosch 실용화</div>
<div class="kb-diagram-note">3. Bron-Kerbosch 실행:</div>
<div class="kb-diagram-note">극대 클리크 열거 (크기 ≥ 3)</div>
<div class="kb-diagram-note">4. 결과 해석:</div>
<div class="kb-diagram-note">클리크 = 단백질 복합체 후보</div>
<div class="kb-diagram-note">GO Term (Gene Ontology) 분석:</div>
<div class="kb-diagram-note">같은 클리크 내 단백질들이 공통 기능 보유하면 유효</div>
<div class="kb-diagram-note">발견 사례:</div>
<div class="kb-diagram-note">크기-5 클리크 {EGFR, GRB2, SOS1, RAS, RAF}</div>
<div class="kb-diagram-note">→ EGFR 신호 경로 복합체</div>
<div class="kb-diagram-note">→ 암 치료 타겟 후보 발견</div>
<div class="kb-diagram-note">성능:</div>
<div class="kb-diagram-note">전체 네트워크: 28,000 노드, 600,000 엣지</div>
<div class="kb-diagram-note">고신뢰도 필터 후: 5,000 노드, 50,000 엣지</div>
<div class="kb-diagram-note">Bron-Kerbosch: ~2분 내 극대 클리크 전체 열거</div>
<div class="kb-diagram-note">한계:</div>
<div class="kb-diagram-note">최대 클리크는 여전히 어려움</div>
<div class="kb-diagram-note">실용: 극대 클리크(Maximal) + 생물학 기반 필터링</div>
<div class="kb-diagram-note">= NP-완전의 실용적 우회</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 단백질 클리크 탐색은 업무 팀 발견 — 병원에서 "이 의사들은 항상 같이 일하네"를 발견하면 팀 구조를 이해할 수 있어요. 단백질 복합체 = 세포 내의 업무 팀!

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클리크 문제 (Clique Problem)</div>
<div class="kb-diagram-note">+-- 이론</div>
<div class="kb-diagram-note">+-- NP-완전 (SAT → 3-SAT → k-Clique)</div>
<div class="kb-diagram-note">+-- 독립 집합과 동치 (여그래프)</div>
<div class="kb-diagram-note">+-- 최대 클리크 = NP-하드</div>
<div class="kb-diagram-note">+-- 알고리즘</div>
<div class="kb-diagram-note">+-- 브루트 포스 O(2^n)</div>
<div class="kb-diagram-note">+-- Bron-Kerbosch (백트래킹)</div>
<div class="kb-diagram-note">+-- 근사 알고리즘 (FPT)</div>
<div class="kb-diagram-note">+-- 응용</div>
<div class="kb-diagram-note">+-- SNS 그룹 탐지</div>
<div class="kb-diagram-note">+-- 단백질 복합체 (생물정보학)</div>
<div class="kb-diagram-note">+-- 추천 시스템</div>
<div class="kb-diagram-note">+-- 관련 문제</div>
<div class="kb-diagram-note">+-- 독립 집합, 버텍스 커버</div>
<div class="kb-diagram-note">+-- 색칠 문제 (Graph Coloring)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[그래프 이론 기초 (1736~)]
Euler 쾨니히스베르크 다리 문제
그래프 기본 개념 확립
      |
      v
[클리크 문제 NP-완전 증명 (1972)]
Karp: SAT → k-Clique 귀납
클리크 ≡ 독립 집합 발견
      |
      v
[Bron-Kerbosch 알고리즘 (1973)]
실용적 극대 클리크 열거
SNS 분석에 활용
      |
      v
[근사 어려움 증명 (1999)]
Hastad: 최대 클리크 근사도 NP-하드
FPT 알고리즘 연구 활발
      |
      v
[대규모 그래프 응용 (2000s~)]
SNS 분석, 생물정보학
준-클리크, k-core 등 완화 개념
      |
      v
[현재: 딥러닝 + 클리크]
GNN 기반 클리크 탐색
대규모 그래프 근사 학습
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클리크는 "모두가 서로 아는 친구 그룹" — 5명이 클리크이려면 5명 중 어떤 두 명을 골라도 반드시 서로 알아야 해요!
2. 클리크 문제는 NP-완전 — 이 그룹을 찾는 가장 빠른 방법이 알려지지 않아서, 빠른 방법을 찾으면 P=NP를 증명한 것!
3. 실용에서는 SNS 그룹 탐지, 단백질 네트워크 분석에 활용 — 완벽한 클리크 대신 "거의 클리크"를 찾는 근사 방법을 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 113 / 175

← **이전**: [007. SAT — 불리언 만족 가능성 문제](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/112_sat/)
**다음**: [009. 버텍스 커버 — Vertex Cover](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/114_vertex_cover/) →

---
