---
title: "Deque, Double-Ended Queue"
date: "2024-03-24"
tags:
  - "datastructure"
  - "studynote-algorithm"
---

## 핵심 인사이트 (3줄 요약)
1. <strong>양방향 입출력</strong>이 가능한 선형 자료구조로, [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))과 큐([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/))의 특성을 모두 결합한 추상 자료형(ADT)이다.
2. 앞(Front)과 뒤(Rear) 양쪽 끝에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삽입 및 삭제가 가능하여 유연한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리가 가능하다.
3. 슬라이딩 윈도우(Sliding Window) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이나 우선순위 조절이 필요한 시스템 스케줄링에 최적화된 구조이다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
덱([Deque](/studynote/08_algorithm_stats/04_datastructure/084_deque/))은 'Double-Ended [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)'의 약자로, 삽입과 삭제가 한쪽 끝에서만 일어나는 제약을 극복하기 위해 설계되었다. [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)(LIFO)으로도, 큐([FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))로도 활용될 수 있는 하이브리드 성격을 지니며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 흐름이 양방향으로 발생해야 하는 복잡한 시스템 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서 핵심적인 역할을 수행한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
덱은 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 또는 이중 [연결 리스트](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)(Doubly [Linked List](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/))를 기반으로 구현되며, 양 끝단에 대한 포인터를 유지한다.

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

| 구분 | 덱 ([Deque](/studynote/08_algorithm_stats/04_datastructure/084_deque/)) | 큐 ([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) ([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/)) |
| :--- | :--- | :--- | :--- |
| **자유도** | 매우 높음 (양방향) | 중간 ([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) | 낮음 ([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) LIFO) |
| **구현 난이도** | 높음 (양방향 포인터 관리) | 낮음 | 매우 낮음 |
| <strong><a href="/studynote/08_algorithm_stats/01_basics/002_time_complexity/">시간 복잡도</a></strong> | 양단 삽입/삭제 O(1) | 삽입/삭제 O(1) | 삽입/삭제 O(1) |
| **슬라이딩 윈도우** | 최적 (양 끝단 관리) | 부적합 | 부적합 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
기술사적 관점에서 덱은 <strong><a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 효율성 극대화</strong>를 위한 도구이다.
1.  **슬라이딩 윈도우 최적화**: 특정 구간의 최댓값/최솟값을 찾을 때, 덱을 사용하여 구간을 벗어난 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 앞(Front)에서 빼고, 새로 들어온 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 뒤(Rear)에서 비교하며 넣어 [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/)를 O(n)으로 유지한다.
2.  <strong>작업 훔치기(<a href="/studynote/02_operating_system/04_synchronization/271_work_stealing/">Work Stealing</a>) <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 멀티코어 환경에서 스케줄러가 자기 큐의 일이 끝나면 다른 프로세서의 덱 뒷부분에서 작업을 가져와 처리함으로써 부하 균형을 맞춘다.
3.  **브라우저 히스토리**: 앞뒤 이동이 빈번한 탐색 기록 관리 등에 유연하게 적용된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
덱은 단순한 저장소를 넘어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 <strong>유연한 <a href="/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/">흐름 제어</a>(<a href="/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/">Flow Control</a>)</strong>를 가능하게 한다. 특히 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스트리밍 처리나 실시간 [그래프 탐색](/studynote/01_computer_architecture/15_advanced_topics/613_graph_bfs_memory/) 시 가변적인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유입에 대응하는 표준적인 방법론을 제공한다. [소프트웨어 아키텍처](/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/) 설계 시 단일 방향 구조의 한계를 느낄 때, 덱은 가장 먼저 고려해야 할 고성능 대안 자료구조이다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
*   **상위 개념**: 선형 자료구조 (Linear [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Structure)
*   **하위/파생 개념**: 입력 제한 덱 (Scroll), 출력 제한 덱 (Shelf), 이중 [연결 리스트](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)
*   <strong>연관 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 슬라이딩 윈도우, 워크 스틸링 ([Work Stealing](/studynote/02_operating_system/04_synchronization/271_work_stealing/)), [BFS](/studynote/08_algorithm_stats/03_graph_search/035_bfs/) (양방향)

### 📈 관련 키워드 및 발전 흐름도

```text
[선형 자료구조 (Linear Data Structure)]
    |
    v
[입력 제한 덱 (Scroll)]
    |
    v
[출력 제한 덱 (Shelf)]
    |
    v
[이중 연결 리스트]
    |
    v
[슬라이딩 윈도우]
```

이 흐름도는 선형 자료구조 (Linear [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Structure)에서 출발해 슬라이딩 윈도우까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 덱은 앞뒤가 똑같은 기차 터널과 같아서, 어느 쪽으로든 기차가 들어가고 나올 수 있어요.
2. 과자 봉지 양쪽을 다 뜯어서, 위로도 꺼내 먹고 밑으로도 꺼내 먹는 것과 비슷해요.
3. [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 큐의 장점만 쏙쏙 골라 합친 변신 로봇 같은 친구랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 175

<- **이전**: [큐 (Queue)](/studynote/08_algorithm_stats/04_datastructure/058_queue/)
**다음**: [이진 트리 (Binary Tree)](/studynote/08_algorithm_stats/04_datastructure/060_binary_tree/) ->

---
