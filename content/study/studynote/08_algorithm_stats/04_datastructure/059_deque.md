+++
weight = 59
title = "덱 (Deque, Double-Ended Queue)"
date = "2024-03-24"
[extra]
categories = ["studynote-algorithm", "datastructure"]
+++

## 핵심 인사이트 (3줄 요약)
1. **양방향 입출력**이 가능한 선형 자료구조로, [[057_stack|스택]]([[057_stack|Stack]])과 큐([[058_queue|Queue]])의 특성을 모두 결합한 추상 자료형(ADT)이다.
2. 앞(Front)과 뒤(Rear) 양쪽 끝에서 [[001_dikw_pyramid|데이터]] 삽입 및 삭제가 가능하여 유연한 [[001_dikw_pyramid|데이터]] 관리가 가능하다.
3. 슬라이딩 윈도우(Sliding Window) [[001_algorithm_definition|알고리즘]]이나 우선순위 조절이 필요한 시스템 스케줄링에 최적화된 구조이다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
덱([[084_deque|Deque]])은 'Double-Ended [[058_queue|Queue]]'의 약자로, 삽입과 삭제가 한쪽 끝에서만 일어나는 제약을 극복하기 위해 설계되었다. [[057_stack|스택]](LIFO)으로도, 큐([[261_fifo_page_replacement|FIFO]])로도 활용될 수 있는 하이브리드 성격을 지니며, [[001_dikw_pyramid|데이터]]의 흐름이 양방향으로 발생해야 하는 복잡한 시스템 [[001_algorithm_definition|알고리즘]]에서 핵심적인 역할을 수행한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
덱은 [[055_array|배열]] 또는 이중 [[056_linked_list|연결 리스트]](Doubly [[056_linked_list|Linked List]])를 기반으로 구현되며, 양 끝단에 대한 포인터를 유지한다.

```text
[ Deque Architecture: Bi-directional Entry ]

     Front Entry                                  Rear Entry
    <-----------> [ [A] | [B] | [C] | [D] ] <----------->
                    Front             Rear

1. Push_Front: 덱의 앞쪽에 데이터 추가
2. Pop_Front: 덱의 앞쪽 데이터 삭제 및 반환
3. Push_Rear: 덱의 뒤쪽에 데이터 추가 (일반 Queue의 Enqueue)
4. Pop_Rear: 덱의 뒤쪽 데이터 삭제 및 반환 (일반 Stack의 Pop)
```

**[특수한 형태의 덱]**
*   **입력 제한 덱 (Scroll)**: 삽입은 한쪽 끝에서만 가능하고, 삭제는 양쪽 끝에서 가능함.
*   **출력 제한 덱 (Shelf)**: 삽입은 양쪽 끝에서 가능하고, 삭제는 한쪽 끝에서만 가능함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 덱 ([[084_deque|Deque]]) | 큐 ([[058_queue|Queue]]) | [[057_stack|스택]] ([[057_stack|Stack]]) |
| :--- | :--- | :--- | :--- |
| **자유도** | 매우 높음 (양방향) | 중간 ([[008_단방향_반이중_전이중|단방향]] [[261_fifo_page_replacement|FIFO]]) | 낮음 ([[008_단방향_반이중_전이중|단방향]] LIFO) |
| **구현 난이도** | 높음 (양방향 포인터 관리) | 낮음 | 매우 낮음 |
| **[[002_time_complexity|시간 복잡도]]** | 양단 삽입/삭제 O(1) | 삽입/삭제 O(1) | 삽입/삭제 O(1) |
| **슬라이딩 윈도우** | 최적 (양 끝단 관리) | 부적합 | 부적합 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
기술사적 관점에서 덱은 **[[001_algorithm_definition|알고리즘]] 효율성 극대화**를 위한 도구이다.
1.  **슬라이딩 윈도우 최적화**: 특정 구간의 최댓값/최솟값을 찾을 때, 덱을 사용하여 구간을 벗어난 [[001_dikw_pyramid|데이터]]는 앞(Front)에서 빼고, 새로 들어온 [[001_dikw_pyramid|데이터]]는 뒤(Rear)에서 비교하며 넣어 [[002_time_complexity|시간 복잡도]]를 O(n)으로 유지한다.
2.  **작업 훔치기([[271_work_stealing|Work Stealing]]) [[001_algorithm_definition|알고리즘]]**: 멀티코어 환경에서 스케줄러가 자기 큐의 일이 끝나면 다른 프로세서의 덱 뒷부분에서 작업을 가져와 처리함으로써 부하 균형을 맞춘다.
3.  **브라우저 히스토리**: 앞뒤 이동이 빈번한 탐색 기록 관리 등에 유연하게 적용된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
덱은 단순한 저장소를 넘어 [[001_dikw_pyramid|데이터]]의 **유연한 [[213_flow_control_buffer_overflow|흐름 제어]]([[421_tcp_flow_control_sliding_window_algorithm|Flow Control]])**를 가능하게 한다. 특히 대용량 [[001_dikw_pyramid|데이터]] 스트리밍 처리나 실시간 [[613_graph_bfs_memory|그래프 탐색]] 시 가변적인 [[001_dikw_pyramid|데이터]] 유입에 대응하는 표준적인 방법론을 제공한다. [[201_software_architecture_definition|소프트웨어 아키텍처]] 설계 시 단일 방향 구조의 한계를 느낄 때, 덱은 가장 먼저 고려해야 할 고성능 대안 자료구조이다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
*   **상위 개념**: 선형 자료구조 (Linear [[001_dikw_pyramid|Data]] Structure)
*   **하위/파생 개념**: 입력 제한 덱 (Scroll), 출력 제한 덱 (Shelf), 이중 [[056_linked_list|연결 리스트]]
*   **연관 [[001_algorithm_definition|알고리즘]]**: 슬라이딩 윈도우, 워크 스틸링 ([[271_work_stealing|Work Stealing]]), [[035_bfs|BFS]] (양방향)

### 📈 관련 키워드 및 발전 흐름도

```text
[선형 자료구조 (Linear Data Structure)]
    │
    ▼
[입력 제한 덱 (Scroll)]
    │
    ▼
[출력 제한 덱 (Shelf)]
    │
    ▼
[이중 연결 리스트]
    │
    ▼
[슬라이딩 윈도우]
```

이 흐름도는 선형 자료구조 (Linear [[001_dikw_pyramid|Data]] Structure)에서 출발해 슬라이딩 윈도우까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 덱은 앞뒤가 똑같은 기차 터널과 같아서, 어느 쪽으로든 기차가 들어가고 나올 수 있어요.
2. 과자 봉지 양쪽을 다 뜯어서, 위로도 꺼내 먹고 밑으로도 꺼내 먹는 것과 비슷해요.
3. [[057_stack|스택]]과 큐의 장점만 쏙쏙 골라 합친 변신 로봇 같은 친구랍니다!
