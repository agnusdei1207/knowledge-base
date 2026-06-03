+++
title = "6. 탐욕 알고리즘 (Greedy Algorithm) — 지역 최적 → 전체 최적"

[taxonomies]
tags = ["algorithm_stats"]

[extra]
tags = ["algorithm_stats"]
+++

# 06. 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Greedy [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(Greedy [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 각 단계에서 그 순간에 가장 최적이라고 판단되는 선택(지역 최적해, Local Optimum)을 하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 설계 패러다임으로, 전체적인 최적해(Global Optimum)를 보장하지는 않는다.
> 2. **가치**: [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)과 달리 하위 문제의 중복 계산이 없으므로 시간 복잡도가 크게 낮아지고, 실제로도 좋은 근사해를 빠르게 얻을 수 있어 실용성이 높다.
> 3. **융합**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 핵심 조건인 <strong>탐욕적 선택 특성(Greedy Choice Property)</strong>과 <strong>최적 부분구조(Optimal Substructure)</strong>는 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)([다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)), [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)([Huffman Coding](/knowledge-base/studynote/08_algorithm_stats/05_string/100_huffman_coding/)), 작업 스케줄링, [최소 신장 트리](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/)([Kruskal](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/), Prim) 등 광범위한 영역에서 적용된다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(Greedy [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 "이 순간에 가장 좋은 것을 선택하라(Do the best you can now)"는 인간의 직관적 의사결정 방식에서 유래했다. 1950년대 컴퓨터 과학자들이 조합 최적화 문제를 풀기 위해 고안한 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은, 각 단계에서 가장 최선을 보는 선택을 함으로써 최종적으로전역 최적해(Global Optimum)에 도달할 수 있다는 희망에서 출발했다. 그러나 이러한 희망이 항상 충족되는 것은 아닌 것이 핵심적인 이다.

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이전역 최적해를 보장하려면 두 가지 조건이 충족되어야 한다. 첫째, **탐욕적 선택 특성(Greedy Choice Property)**: 이전에 수행한 선택과 무관하게 매 단계에서 지역적으로 최적인 선택이전역적으로도 최적인 해로 이어질 수 있는 특성이다. 둘째, **최적 부분구조(Optimal Substructure)**: 문제의 최적해가 하위 문제의 최적해들로 구성되는 구조이다. 이 두 조건이 모두 만족되면 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이전역 최적해를 보장한다.

> 이 도식은 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 원리와 한계를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕 알고리즘의 작동 원리와 한계</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕 알고리즘의 결정 트리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제 시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선택 A (가장 좋음) 선택 B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선택 A-1 선택 A-2 ← 이 순간 가장 좋은 것을 선택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선택 A-1-a</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">지역 최적해 ×</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">최종 해가전역 최적해라는 보장은 없음</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕이 실패하는 경우: 거스름돈 문제</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">동전: 1원, 4원, 5원</div><div class="kb-diagram-cell">목표: 10원</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐욕: 5원 → 5원 → 1원+1원+1원+1원+1원 = 5개 동전</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(5원 선택 → 5원 선택 → 남은 0원? No → 1원 반복)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 5 + 4 + 1 = 10원 = 3개</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 최적: 5 + 5 = 2개 (탐욕 = 5개 vs 최적 = 2개)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이유: 탐욕적 선택(가장 큰 동전)이전역 최적해로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이어지지 않음 → 탐욕 선택 특성을 만족하지 않음</div></div>
</div>
</div>



- **관찰**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 실패하는 경우는 "지역 최적해에서전역 최적해로" 이어지지 않는 구조적 문제가 있는 경우이다.
- **원인**: 거스름돈 문제에서 4원을 선택하지 않고 5원을 선택한 것은 지역적으로는 optimal하지만(가장 큰 값), 전체적으로는 5+5가 5+4+1보다 동전 수가 적다.
- **결과**: 모든 문제에 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 적용할 수 있는 것이 아니라, 탐욕 선택 특성을 만족하는 문제만을 대상으로 해야 한다.
- **판단**: 문제의 분석에서 "탐욕적 선택이전역 최적해로 이어지는가?"를 판단하는 것이 가장 중요하며, 이것이 기술사 시험의 핵심이다.

📢 **섹션 요약 비유**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 등산에서 산을 오를 때 "지금 갈 수 있는 길 중 가장 가파른 길을 선택하는 것"과 같습니다. 당장은 빠르게 올라가는 것 같지만, 표기되지 않은 고난도 루트를 만나거나 벌새에 갇혀전역적으로 정상(최적해)에 도달하지 못할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 구조는 [동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/)(DP)과 비교하면 매우 단순하다. DP가 모든 하위 문제의 해를표로 저장하고bottom-up으로 결합하다의에、탐욕은 매 단계에서 가장 좋은 선택을하고 더 이상 이전 선택을 고려하지 않는다. 이 차이는 시간 복잡도에서 극명한 차이로 나타난다. DP의 피보나치는 O(N) 시간과 O(N) 공간이지만, 최적 부분구조와 탐욕 선택 특성이 있는 경우 탐욕은 O(N) 시간과 O(1) 공간으로 동일한 결과를낸다.

<strong>탐욕 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>이 적용 가능한 대표 문제</strong>를 살펴보면, <strong>활동 선택 문제(Activity <a href="/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/">Selection</a> Problem)</strong>: 회의실 하나에 최대한 많은 활동을 배치하는 문제로, 가장 빨리 끝나는 활동을 선택하는 탐욕 전략이전역 최적해를 보장한다. <strong>분수 배낭 문제(Fractional <a href="/knowledge-base/studynote/08_algorithm_stats/06_np_theory/116_knapsack/">Knapsack</a>)</strong>: 배낭에을 넣을 때 무게 대비 가치 비율이 가장 높은부터 넣는 탐욕 전략이전역 최적해를 보장한다(다만 0/1 배낭 문제에서는 탐욕이). <strong>유클리드 호제법(<a href="/knowledge-base/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/">GCD</a>)</strong>: 두 수의 최대공약수에서 나머지가 0이 될 때까지 큰 수를 작은수로 나누는 과정이 탐욕적 선택의 대표적 사례이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕 vs 동적 프로그래밍 비교</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">피보나치로 비교</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DP (Bottom-up, 타뷸레이션):</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">0</div><div class="kb-diagram-note">=0, dp</div><div class="kb-diagram-node">1</div><div class="kb-diagram-note">=1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">for i=2 to N:</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-note">+ dp</div><div class="kb-diagram-node">i-2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ O(N) 시간, O(N) 공간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Greedy (활동 선택 등, 특화된 경우):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">: 피보나치에는 직접 적용 불가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">: "가장 빠른 종료" 선택 → 활동 선택 문제에 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ O(N) 시간, O(1) 공간 (DP보다 적은 자원)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">활동 선택 문제에 적용</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">활동:</div><div class="kb-diagram-node">(시작, 종료), ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">입력: (1,4), (3,5), (0,6), (5,7), (3,9), (5,9),</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(6,10), (8,11), (8,12), (2,14), (12,16)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐욕 적용: 종료 시간이 가장 빠른 순으로 정렬</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ (1,4), (3,5), (5,7), (6,10), (8,11), (8,12),</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(12,16)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선택: (1,4) 선택 → 이후 활동 (3,5) 선택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 최대 활동 수: 6개 (탐욕이전역 최적해 보장)</div></div>
</div>
</div>



- **관찰**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 하위 문제의 해를 저장하지 않고 매 단계의 결정만 하므로, DP보다 시간과 공간을 절약할 수 있다.
- **원인**: 탐욕 선택 특성이 있으면, 각 단계의 최적해가전역 최적해의 일부가 되므로, 이전 선택을할 필요가 없기 때문이다.
- **결과**: 이 속성을 가진 문제에서는 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 DP보다 훨씬 효율적으로 동일한 최적해를 찾는다.
- **판단**: 탐욕으로 풀 수 있는 문제는 항상 DP로도 풀리지만, 그 반대는 성립하지 않는다. 따라서 문제를 분석할 때 "탐욕 선택 특성을 만족하는가?"를 먼저 확인해야 한다.

📢 **섹션 요약 비유**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 연쇄 으로 물건을 파는 상인과 같습니다. 오늘 가장 비싸게 팔 수 있는 가격에 책을 팔고, 내일의 상황은 나중에하는 것은、단기적으로는을하지만, 전체적으로는하는 선택을 할 수 있습니다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

실무에서 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 <strong>신뢰할 수 있는 빠른 해</strong>가 필요한 경우에 사용된다. 전역 최적해를 보장하지 않더라도, 거의 최적에 가까운 해를 매우 빠르게 얻을 수 있으므로, 실시간 시스템이나 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리에서 유용하다.

<strong>대표적 실무 사례</strong>로, <strong><a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">다익스트라</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/">Dijkstra</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 각 단계에서 아직 방문하지 않은 정점 중 최단 거리가 가장 가까운 것을 선택하는 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 음수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 없는 그래프에서 단일 출발점 최단 경로를 보장한다. <strong>프림(Prim) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: [최소 신장 트리](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/)(Minimum Spanning Tree)를 구성할 때, 현재 트리에 연결 가능한 간선 중 최소 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 간선을 선택하는 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. <strong>크루스컬(<a href="/knowledge-base/studynote/08_algorithm_stats/03_graph_search/042_kruskal/">Kruskal</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 모든 간선을 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 순으로 정렬하고, 사이클을 형성하지 않는 간선을 선택하는 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/05_string/100_huffman_coding/">허프만 코딩</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/05_string/100_huffman_coding/">Huffman Coding</a>)</strong>: 문자열 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)에서 출현 빈도가 높은 문자에게 짧은 코드를 부여하기 위해, 가장 빈도가 낮은 두 노드를하는 과정을 반복하는 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">다익스트라 알고리즘: 탐욕의 대표 사례</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그래프</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A ---4--- B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2</div><div class="kb-diagram-cell">\ 5</div><div class="kb-diagram-cell">1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C ---3--- D ---2--- E</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">다익스트라 (출발점: A)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Step 0: A = {A}, distance</div><div class="kb-diagram-node">A</div><div class="kb-diagram-note">= 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Step 1: A에서 갈 수 있는 정점 중 최단:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A→B=4, A→C=2, A→D=∞</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ C 선택 (가장 짧음: 2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A = {A, C}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Step 2: C에서 새로 도달 가능한 정점 업데이트:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A→B via C = 2+3=5 &lt; 현재 4? No → 유지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A→D via C = 2+3=5 → D = 5</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ B 선택 (가장 짧음: 4)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A = {A, C, B}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Step 3: B에서 업데이트, D via B = 4+1=5 = D 현재값</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ D 선택 (4)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A = {A, C, B, D}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Step 4: E 선택 (5+2=7)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">최종: A→B=4, A→C=2, A→D=5, A→E=7</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 각 단계에서 가장 짧은 정점을 선택하는 탐욕</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 전역 최단 경로 보장 (음이 아닌 가중치)</div></div>
</div>
</div>



📢 **섹션 요약 비유**: [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/)의 탐욕 선택은 교차로에서 가장 짧은 거리를 선택하는 내비게이션과 같습니다. "지금은 이 길이 가장 빠르니까"라는 판단만 하고, 다른 경로를 고려하지 않지만, 고속도로 부울럼이 없는 한（음이 아닌 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)) 이 판단은 결국 전역적으로도 가장 빠른 경로로 이어집니다.

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 품질 관리에서 가장 중요한 것은 <strong>탐욕 선택 특성의 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>이다. 문제가 실제로 탐욕 선택 특성을 만족하는지 엄밀한 수학적 없이 적용하면, 예상외의 suboptimal 해가 도출될 수 있다.

<strong>품질 관리 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>는 다음과 같다. 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 적용 전 반드시 "탐욕 선택 특성이 존재하는가?"를 수학적/논리적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다. 최악의 경우(입력이 극단적으로 불균형)에도 해의 품질이 가능한 수준인지 확인해야 한다. 근사 비율(Approximation Ratio)을 명시적으로하여 요구사항을 만족하는지 확인해야 한다.

📢 **섹션 요약 비유**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 품질 관리는 미식 축구에서 매 번 가장 가까운 터치다운을 하는 것과 같습니다. 그 순간은 brilliant해 보이지만, 결국 경기에서 진급하려면 적인 전략이 필요하듯이, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없는 탐욕 적용은 전역 최적에서 멀어지는 결과를 초래할 수 있습니다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 최신 동향은 <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">앙상블</a> 방법(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">Ensemble</a> Methods)</strong>과의 결합이다. 머신러닝에서 <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/077_Adaboost/">AdaBoost</a></strong>는 각 단계에서 가장 오류가 적은 분류기(Weak Classifier)를 탐욕적으로 선택하여 최종 강 분류기(Strong Classifier)를 구축한다. 또한 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/">근사 알고리즘</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/">Approximation Algorithm</a>)</strong> 분야에서 탐욕이 이론적(Approximation Ratio)을 보장하는 연구가 활발히 진행되고 있다.

탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 모든 문제에 적용할 수는 없지만, 적용 가능한 문제에서는 압도적인 효율성(시간 O(N), 공간 O(1))으로 동일한 최적해를 보장한다. 기술사 시험에서는 특정 문제가 탐욕으로 풀리는지 DP로 풀리는지를 구분하는 능력과, 그 근거를설명할 수 있는 능력을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

📢 **섹션 요약 비유**: 탐욕 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 요리와 같습니다. 레시피 대로 천천히 조리하면(DP) 확실히 맛있지만, 시간 없을 때"Just 맛볼 재료를 먼저어()"라는 탐욕적 접근은 완전하지는 않더라도 충분히 맛있는 요리가 될 수 있습니다.

---

## 핵심 인사이트 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 ([Concept](/knowledge-base/studynote/14_data_engineering/02_math_mining/120_concept/) Map)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕 알고리즘 (Greedy Algorithm) 핵심 개념 맵</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐욕 알고리즘 (Greedy Algorithm)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">핵심 조건</div><div class="kb-diagram-cell">알고리즘 구조</div><div class="kb-diagram-cell">대표 사례</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Conditions</div><div class="kb-diagram-cell">Structure</div><div class="kb-diagram-cell">Examples</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐욕 선택 특성</div><div class="kb-diagram-cell">1. 후보들 중</div><div class="kb-diagram-cell">다익스트라</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Greedy Choice</div><div class="kb-diagram-cell">최적 선택</div><div class="kb-diagram-cell">Prim MST</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">최적 부분구조</div><div class="kb-diagram-cell">2. 선택 후</div><div class="kb-diagram-cell">Kruskal MST</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Optimal Sub</div><div class="kb-diagram-cell">제한 검사</div><div class="kb-diagram-cell">Huffman Coding</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 종료/계속</div><div class="kb-diagram-cell">활동 선택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 해 구성</div><div class="kb-diagram-cell">분수 배낭</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Greedy vs DP vs Brute Force</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Greedy: O(N) ~ O(N log N), 최적해 보장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DP: O(N²) ~ O(2^N), 항상 최적해 보장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BF: O(2^N) ~ O(N!), 항상 최적해 보장</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">적용 가능 판단 기준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐욕 선택 특성 + 최적 부분구조 → Greedy</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중복 하위 문제 + 최적 부분구조 → DP</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">둘 다 안 되면 → 근사 or BF</div></div>
</div>
</div>



### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **최적 부분 구조** | 큰 문제를 작은 최적 해로 나눌 수 있는 성질 |
| **탐욕 선택** | 매 단계에서 가장 좋아 보이는 선택을 하는 원리 |
| <strong>그리디 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | 이 원리를 실제 문제 해결에 적용하는 방법 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/">근사 알고리즘</a></strong> | 최적 해가 어려울 때 현실적인 해를 찾는 확장 |
### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">최적 부분 구조 (Optimal Substructure)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">탐욕 선택 (Greedy Choice)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그리디 알고리즘 (Greedy Algorithm)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">근사 알고리즘 (Approximation Algorithm)</div></div>
</div>
</div>



이 흐름도는 문제의 구조를 이용해 탐욕 선택이 그리디 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 근사 해법으로 이어지는 과정을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

1. 매번 가장 좋아 보이는 선택을 하는 전략이다.
2. 정답이 보장되려면 문제에 특별한 성질이 필요하다.
3. 그래서 최적이 어려우면 [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)으로 이어진다.
## 참고
- 모든 약어는 반드시 전체 명칭과 함께 표기
- 일어/중국어 절대 사용 금지
- 각 섹션 끝에 📢 요약 비유 반드시 추가
- 최소 800자/[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)
- [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)명: 01_, 02_... 형식

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 6 / 175

← **이전**: [5. 분할 정복 (Divide and Conquer) — 재귀 분할 + 병합](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)
**다음**: [7. 동적 프로그래밍 (Dynamic Programming) — 최적 부분구조 + 중복 부분 문제](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/) →

---
