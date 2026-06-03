---
title: 큐 (Queue)
date: '2024-03-24'
tags:
- datastructure
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)
1. **[[261_fifo_page_replacement|FIFO]](First-In, First-Out)** 원칙에 따라 먼저 삽입된 [[001_dikw_pyramid|데이터]]가 먼저 제거되는 선형 자료구조이다.
2. 삽입 연산은 **Enqueue(Rear)**, 제거 연산은 **Dequeue(Front)**를 통해 수행되며, 주로 대기열 관리 및 [[001_dikw_pyramid|데이터]] 버퍼링에 활용된다.
3. 원형 큐(Circular Queue)를 통해 선형 큐의 메모리 낭비 문제를 해결하며, 시간 복잡도는 삽입/삭제 모두 **O(1)**을 보장한다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
큐(Queue)는 일상생활의 '줄 서기'와 동일한 논리적 구조를 가진 추상 자료형(ADT)이다. [[057_stack|스택]]([[057_stack|Stack]])의 LIFO와 대조되는 **[[261_fifo_page_replacement|FIFO]](선착순)** 방식을 따르며, 운영체제의 프로세스 스케줄링, 네트워크 패킷 전송 대기열, 프린터 출력 대기열 등 [[017_hardware_interrupt|비동기적]] [[001_dikw_pyramid|데이터]] 전송이 필요한 시스템 아키텍처의 핵심 요소이다. 특히 CPU와 주변 기기 간의 속도 차이를 보완하는 **버퍼(Buffer)**로서의 역할이 매우 중요하다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
큐의 구조는 [[001_dikw_pyramid|데이터]]를 넣는 뒤쪽인 Rear와 [[001_dikw_pyramid|데이터]]를 빼는 앞쪽인 Front로 구성된다.

```text
[ Queue Architecture: FIFO Principle ]

     Enqueue (Rear)                               Dequeue (Front)
    ---------------> [ [D] | [C] | [B] | [A] ] --------------->
                       Rear             Front

1. Enqueue: Rear 위치에 새로운 요소 추가 (Rear = Rear + 1)
2. Dequeue: Front 위치의 요소 제거 및 반환 (Front = Front + 1)
3. Peek/Front: 제거 없이 가장 앞에 있는 요소 확인
4. IsEmpty/IsFull: 큐의 상태 확인
```

**[선형 큐 vs 원형 큐 (Linear vs Circular)]**
*   **선형 큐(Linear Queue)**: [[055_array|배열]]의 끝까지 [[001_dikw_pyramid|데이터]]를 채우면 앞쪽이 비어 있어도 활용하지 못하는 단점이 있음.
*   **원형 큐(Circular Queue)**: 마지막 인덱스에서 다음 인덱스가 0으로 연결되는 구조 `(index + 1) % Size`를 사용하여 공간을 효율적으로 재사용함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 큐 (Queue) | [[057_stack|스택]] ([[057_stack|Stack]]) | 덱 ([[084_deque|Deque]]) |
| :--- | :--- | :--- | :--- |
| **원칙** | [[261_fifo_page_replacement|FIFO]] (First-In, First-Out) | LIFO (Last-In, First-Out) | 양방향 입출력 가능 |
| **핵심 연산** | Enqueue (Rear), Dequeue (Front) | Push (Top), [[120_pop_point_of_production|Pop]] (Top) | Push_Front/Back, Pop_Front/Back |
| **주요 용도** | 프로세스 스케줄링, 버퍼, [[035_bfs|BFS]] | [[014_recursion|재귀]] 함수, 실행 취소, [[034_dfs|DFS]] | 슬라이딩 윈도우, 스케줄링 |
| **메모리 활용** | 원형 구조 권장 (공간 효율) | 단순 [[055_array|배열]]/[[056_linked_list|연결 리스트]] | 동적 할당 [[055_array|배열]] (Vector 등) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
기술사적 관점에서 큐는 **시스템 부하 [[136_variance|분산]]([[196_hard_soft_real_time|Load Balancing]])**의 중추이다.
1.  **메시지 큐(Message Queue)**: [[179_kafka_flink_watermark_time_window|Kafka]], RabbitMQ 등 [[136_variance|분산]] 시스템에서 [[603_component_independent_deployment_unit|컴포넌트]] 간 결합도를 낮추고 비동기 처리를 통해 확장성을 확보할 때 활용된다.
2.  **[[083_priority_queue|우선순위 큐]]([[083_priority_queue|Priority Queue]])**: 단순 FIFO가 아닌 우선순위에 따른 처리가 필요할 때 힙([[078_heap_datastructure|Heap]]) 자료구조와 융합하여 구현하며, 운영체제의 우선순위 스케줄링에 사용된다.
3.  **[[282_performance_tactics|성능]] 최적화**: [[055_array|배열]] 기반 구현 시 원형 큐를 사용하여 공간 복잡도를 최적화하고, 크기가 가변적인 경우 [[056_linked_list|연결 리스트]] 기반 큐를 사용하여 오버플로우를 방지한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
큐는 [[001_dikw_pyramid|데이터]] 전송의 안정성과 공정성을 보장하는 가장 기본적인 도구이다. 현대 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서 [[206_serverless_cold_start|서버리스]] 아키텍처의 이벤트 [[507_acid_properties|트리거]], [[532_microservices_decomposition_patterns|마이크로서비스]] 간 통신 규약으로서 큐의 위상은 더욱 높아지고 있다. 단순히 [[001_dikw_pyramid|데이터]]를 저장하는 자료구조를 넘어, 시스템 간의 **속도 완충기(Speed Buffer)**이자 **안정성 보장 장치**로서의 표준적 지위를 유지할 것이다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
*   **상위 개념**: 선형 자료구조 (Linear [[001_dikw_pyramid|Data]] Structure)
*   **하위/파생 개념**: 원형 큐 (Circular Queue), [[083_priority_queue|우선순위 큐]] ([[083_priority_queue|Priority Queue]]), 덱 ([[084_deque|Deque]]), 메시지 큐 (MQ)
*   **연관 [[001_algorithm_definition|알고리즘]]**: [[035_bfs|BFS]] ([[035_bfs|너비 우선 탐색]]), [[036_dijkstra|다익스트라]] ([[036_dijkstra|Dijkstra]])

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 선형 자료구조 (Linear Data Structure)]
    │
    ▼
[하위/파생 개념: 원형 큐 (Circular Queue), 우선순위 큐 (Priority Queue), 덱 (Deque), 메시지 큐 (MQ)]
    │
    ▼
[연관 알고리즘: BFS (너비 우선 탐색), 다익스트라 (Dijkstra)]
```

이 흐름도는 상위 개념: 선형 자료구조 (Linear [[001_dikw_pyramid|Data]] Structure)에서 출발해 연관 [[001_algorithm_definition|알고리즘]]: [[035_bfs|BFS]] ([[035_bfs|너비 우선 탐색]]), [[036_dijkstra|다익스트라]] ([[036_dijkstra|Dijkstra]])까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 큐는 편의점에서 물건을 살 때 기다리는 '줄'과 같아요.
2. 먼저 온 사람이 먼저 계산하고 나가는 아주 공평한 규칙이에요.
3. 기차 터널처럼 한쪽으로 들어가서 반대쪽으로 나오는 것과 같답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 175

← **이전**: [[057_stack|3. 스택 (Stack) — LIFO, push/pop, 재귀/DFS/수식 평가]]
**다음**: [[059_deque|덱 (Deque, Double-Ended Queue)]] →

---
