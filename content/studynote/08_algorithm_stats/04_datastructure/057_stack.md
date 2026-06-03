+++
title = "3. 스택 (Stack) — LIFO, push/pop, 재귀/DFS/수식 평가"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스택 (Stack)은 LIFO (Last In First Out) 원칙에 따라 가장 나중에 삽입된 원소가 가장 먼저 제거되는 선형 자료구조로, push·[pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/)·peek 모두 O(1)이다.
> 2. **가치**: [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 스택([재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)), [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) (Depth-First Search), 수식 평가, 괄호 검사 등 "가장 최근 상태로 되돌아가야 하는" 모든 문제가 스택 한 줄로 풀린다.
> 3. **판단 포인트**: 역순 처리·[백트래킹](/knowledge-base/studynote/08_algorithm_stats/01_basics/010_backtracking/)·중첩 구조 파싱이 등장하면 스택을, 순서대로 처리해야 하면 큐를 선택한다.

---

## Ⅰ. 개요 및 필요성

스택은 "마지막에 넣은 것을 먼저 꺼낸다"는 LIFO 규칙 하나로 정의된다. 현실에서는 식판 쌓기, 실행 취소([Undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/)) 버튼, 웹 브라우저의 뒤로 가기가 모두 스택 구조다. CPU도 함수를 호출할 때마다 반환 주소·지역 변수를 스택 프레임에 쌓고, 함수가 끝나면 팝([Pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/))하여 호출 이전 상태로 복원한다.

### 스택 기본 연산

| 연산 | 설명 | [시간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/002_time_complexity/) |
|:---|:---|:---:|
| push(x) | 원소 x를 맨 위에 삽입 | O(1) |
| [pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/)() | 맨 위 원소 제거 후 반환 | O(1) |
| peek() / top() | 맨 위 원소 조회(제거 없음) | O(1) |
| isEmpty() | 스택 비어 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | O(1) |

📢 **섹션 요약 비유**: 스택은 뷔페 식판 더미다—항상 맨 위 식판만 집을 수 있고, 반납할 때도 맨 위에 올린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 기반 스택 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">top = 3</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">10</div><div class="kb-diagram-cell">20</div><div class="kb-diagram-cell">30</div><div class="kb-diagram-cell">40</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">0</div><div class="kb-diagram-node">1</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">3</div><div class="kb-diagram-node">4</div><div class="kb-diagram-node">5</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">push(50): arr</div><div class="kb-diagram-node">4</div><div class="kb-diagram-note">=50, top=4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">pop() : return arr</div><div class="kb-diagram-node">4</div><div class="kb-diagram-note">=50, top=3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">peek() : return arr</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">=40</div></div>
</div>
</div>



<strong>스택 오버플로 (Stack <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/">Overflow</a>)</strong>: 고정 크기 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 기반 스택에서 top이 capacity를 초과할 때 발생. [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 깊이가 지나치게 깊을 때 OS가 스택 세그먼트를 초과하여 발생하는 오류와 같은 원리다.

### [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 스택 ([Call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Stack)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">main() 호출 → factorial(3) 호출 → factorial(2) 호출 → factorial(1)</div>
<div class="kb-diagram-note">Call Stack:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">factorial(1) frame</div><div class="kb-diagram-cell">← top (실행 중)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">factorial(2) frame</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">factorial(3) frame</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">main() frame</div><div class="kb-diagram-cell">← bottom</div></div>
<div class="kb-diagram-note">factorial(1) 반환 → pop, factorial(2) 재개 → pop → ...</div>
</div>
</div>



### 수식 평가: 중위 → 후위 (Infix → Postfix, Shunting-yard)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">입력: 3 + 4 * 2 (중위 표기)</div>
<div class="kb-diagram-note">출력: 3 4 2 * + (후위 표기, 스택 활용)</div>
<div class="kb-diagram-note">처리 과정:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기</div><div class="kb-diagram-cell">출력</div><div class="kb-diagram-cell">연산자 스택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3</div><div class="kb-diagram-cell">3</div><div class="kb-diagram-cell">[]</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">+ │ 3</div><div class="kb-diagram-node">+</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">4 │ 3 4</div><div class="kb-diagram-node">+</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">* │ 3 4</div><div class="kb-diagram-node">+, *</div><div class="kb-diagram-note">(* 우선순위 &gt; +)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">2 │ 3 4 2</div><div class="kb-diagram-node">+, *</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">끝</div><div class="kb-diagram-cell">3 4 2 * +</div><div class="kb-diagram-cell">[]</div></div>
</div>
</div>



📢 **섹션 요약 비유**: 수식 평가에서 스택은 아직 처리 못 한 연산자를 잠시 보관하는 대기줄—우선순위 높은 연산자가 먼저 처리될 때까지 낮은 것들이 기다린다.

---

## Ⅲ. 비교 및 연결

### 스택 vs 큐 vs 덱

| 항목 | 스택 | 큐 ([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | 덱 ([Deque](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/)) |
|:---|:---:|:---:|:---:|
| 삽입 위치 | top | rear | both ends |
| 제거 위치 | top | front | both ends |
| 원칙 | LIFO | [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) | 양방향 |
| 주요 활용 | [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/), [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/), [undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/) | [BFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/035_bfs/), 스케줄링 | 슬라이딩 윈도우 |

### 스택과 [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/)

[DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) (Depth-First Search)는 방문 경로를 스택에 쌓고, 막히면 pop하여 이전 분기로 돌아간다. [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) DFS는 암묵적으로 콜 스택을 활용하며, 반복 DFS는 명시적 스택을 사용한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">그래프: A─B─D</div>
<div class="kb-diagram-tree-item" style="--depth:4">C─E</div>
<div class="kb-diagram-note">재귀 DFS 콜 스택:</div>
<div class="kb-diagram-note">visit(A) → visit(B) → visit(D) ← pop</div>
<div class="kb-diagram-note">→ visit(C) → visit(E) ← pop</div>
</div>
</div>



📢 **섹션 요약 비유**: DFS는 미로 탐색자가 "지금 온 길"을 손바닥에 메모하면서 벽이 막히면 메모를 지우고 마지막 갈림길로 돌아가는 전략이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **괄호 검사**: `{[()]}` 올바른지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)—열린 괄호를 push, 닫힌 괄호 만날 때 pop하여 쌍 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- **브라우저 뒤로 가기**: 방문 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) URL 스택 + 앞으로 가기 스택(두 스택으로 구현)
- **컴파일러 파싱**: [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 하강 파서의 파싱 스택, AST (Abstract Syntax Tree) 구성
- <strong>텍스트 편집기 <a href="/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/">Undo</a>/<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/">Redo</a></strong>: 변경 이력 스택 두 개([undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/) 스택 + [redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 스택)
- <strong>모노토닉 스택 (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/079_monotonic_stack/">Monotonic Stack</a>)</strong>: 다음 큰 원소(NGE), 히스토그램 최대 직사각형

### 스택 구현 선택



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">크기 고정 + 성능 우선 → 배열 기반 스택 (캐시 친화적)</div>
<div class="kb-diagram-note">크기 무제한 + 유연성 → 연결 리스트 기반 스택</div>
<div class="kb-diagram-note">재귀 깊이 제어 필요 → 명시적 스택으로 재귀 대체 (Stack Overflow 방지)</div>
</div>
</div>



📢 **섹션 요약 비유**: 컴파일러에서 스택 없이 중첩 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)이나 괄호를 처리하는 것은 "몇 겹을 열었는지" 기억하지 않고 러시안 마트료시카를 조립하려는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

스택은 단순한 구조임에도 불구하고 시스템 소프트웨어부터 응용 알고리즘까지 광범위하게 사용된다. push·[pop](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/) O(1)의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 구현 용이성, 그리고 LIFO라는 직관적 의미론이 결합되어 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)적 문제 해결의 표준 도구가 되었다. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)로 구현하면 캐시 친화적이고, 연결 리스트로 구현하면 크기 제한이 없다.

**결론**: "가장 최근 것을 먼저"라는 패턴이 있는 모든 문제—[재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/), [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/), 수식 평가, 괄호 검사, [undo](/knowledge-base/studynote/11_design_supervision/06_exam_summary/393_undo/)—에서 스택은 1순위 선택이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| 큐 ([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 대칭 구조 |
| [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) ([Recursion](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)) | 콜 스택 = 암묵적 스택 |
| [DFS](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/034_dfs/) | 스택으로 구현하는 탐색 |
| 모노토닉 스택 | 단조성 조건 추가한 스택 응용 |
| 수식 평가 (Expression) | 중위→후위 변환에 스택 활용 |
| 후위 표기법 (Postfix) | 스택으로 O(n) 계산 |

---

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">:---</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">큐 (Queue)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">재귀 (Recursion)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DFS</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">모노토닉 스택</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">수식 평가 (Expression)</div></div>
</div>
</div>



이 흐름도는 :---에서 출발해 모노토닉 스택까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스택은 쌓인 접시더미야—항상 맨 위 접시만 집을 수 있고, 새 접시도 맨 위에 올려.
2. 컴퓨터도 함수를 부를 때마다 "어디서 왔는지"를 스택에 기록해서, 함수가 끝나면 원래 자리로 돌아와.
3. 괄호 검사도 여는 괄호가 나오면 쌓고, 닫는 괄호가 나오면 맨 위를 꺼내 짝이 맞는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 돼.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 175

← **이전**: [2. 연결 리스트 (Linked List) — 단일/이중/순환](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)
**다음**: [큐 (Queue)](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) →

---
