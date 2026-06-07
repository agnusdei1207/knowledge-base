---
title: "Stack / Queue"
date: "2026-06-07"
tags:
  - "it_management"
  - "studynote-it-management"
weight: 852
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))은 LIFO, 큐([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/))는 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 원칙을 따르는 기본 자료 구조다.
> 2. **가치**: 호출 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/), 작업 대기열, [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/)/[DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/) 등에서 자주 쓰인다.
> 3. **판단**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름의 순서를 설계할 때 가장 먼저 떠올려야 하는 기본 도구다.

---

## Ⅰ. 개요 및 필요성

[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐는 자료 구조의 가장 기본적인 두 축이다. 순서를 어떻게 처리할지에 따라 둘 중 하나를 고르면 된다.

단순하지만 활용 범위가 매우 넓다.

- **📢 섹션 요약 비유**: 접시를 쌓아 두는 방식과 줄을 서는 방식의 차이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Stack: push / pop
Queue: enqueue / dequeue
```

| 구조 | 원리 | 예 |
| :-- | :-- | :-- |
| [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | LIFO | [함수 호출](/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/), 되돌리기 |
| [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) | [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) | 작업 대기, [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) |

[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 마지막에 넣은 것이 먼저 나오고, 큐는 먼저 들어온 것이 먼저 나온다.

- **📢 섹션 요약 비유**: 나중에 놓은 책이 맨 위, 먼저 온 손님이 먼저 입장하는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) |
| :-- | :-- | :-- |
| 순서 | LIFO | [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) |
| 주요 연산 | push/[pop](/studynote/07_enterprise_systems/02_erp_systems/120_pop_point_of_production/) | enqueue/dequeue |
| 용도 | [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/)/역추적 | 스케줄링/대기열 |

| 관련 개념 | 의미 |
| :-- | :-- |
| [Deque](/studynote/08_algorithm_stats/04_datastructure/084_deque/) | 양방향 |
| Circular [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) | 원형 큐 |

[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐는 알고리즘의 흐름과 운영 시스템의 작업 처리에서 모두 중요하다.

- **📢 섹션 요약 비유**: 쌓는지, 줄 세우는지에 따라 처리 방식이 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. LIFO와 FIFO를 구분하는가?
2. 연산의 시간 복잡도를 아는가?
3. [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 오버플로/언더플로를 고려하는가?
4. 큐의 병목과 순서를 관리하는가?
5. 상황에 맞는 구조를 고르는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐를 혼동하는 설계
- 대기열 순서를 무시하는 설계
- [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 깊이와 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 한계를 무시하는 설계
- 목적 없이 자료 구조를 선택하는 설계

기술사 관점에서는 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐를 "순서 제어의 기본 자료 구조"로 설명해야 한다.

- **📢 섹션 요약 비유**: 쌓을지, 줄 설지 먼저 정해야 한다.

---

## Ⅴ. 기대효과 및 결론

[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐를 이해하면 알고리즘과 시스템 설계를 더 명확히 할 수 있다.

결론적으로 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 LIFO, 큐는 FIFO를 구현하는 기본 자료 구조다.

- **📢 섹션 요약 비유**: 순서가 바뀌면 결과도 달라진다.

---

## 관련 개념 맵

```text
Stack
  v
LIFO
  v
Queue
  v
FIFO
```

---

## 관련 키워드 및 발전 흐름도

```text
List
  v
Stack / Queue
  v
Deque
  v
Scheduling / Traversal
```

---

## 어린이를 위한 3줄 비유 설명

쌓아 두면 나중에 올린 게 먼저 나와요.
줄 서면 먼저 온 사람이 먼저 가요.
[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐는 그런 순서예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 587

<- **이전**: [68. 지속적 서비스 개선 (CSI, Continual Service Improvement)](/studynote/12_it_management/02_itsm_itil/068_csi/)
**다음**: [69. 데크/원형 큐 (Deque / Circular Queue)](/studynote/12_it_management/02_itsm_itil/069_deque_circular_queue/) ->

---
