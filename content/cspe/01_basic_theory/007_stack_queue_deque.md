---
title: "스택·큐·덱 (Stack Queue Deque)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 7
---

# 스택·큐·덱 (Stack, Queue, Deque)

## 1. 정의 및 개념

| 구분 | 정의 | 연산 원리 |
|---|---|---|
| **스택(Stack)** | 삽입과 삭제가 한쪽 끝(Top)에서만 일어나는 선형 자료구조 | **LIFO**(Last In First Out) |
| **큐(Queue)** | 삽입은 후단(Rear), 삭제는 전단(Front)에서 일어나는 선형 자료구조 | **FIFO**(First In First Out) |
| **덱(Deque, Double-Ended Queue)** | 양쪽 끝(Front, Rear) 모두에서 삽입·삭제가 가능한 선형 자료구조 | 스택과 큐의 일반화 |

스택·큐·덱은 내부 구현보다 데이터가 어떤 순서로 들어가고 나오는지가 핵심인 추상 자료형(Abstract Data Type, ADT)이다.

## 2. 구조 및 주요 연산

**스택**
- push: Top에 원소 삽입
- pop: Top 원소 삭제 및 반환
- peek/top: 최상단 원소 조회
- isEmpty/isFull: 언더플로우·오버플로우 검사
- 배열 구현 시 top 포인터로 관리

**큐**
- enqueue: Rear에 원소 삽입
- dequeue: Front 원소 삭제 및 반환
- front/rear 포인터 관리
- 선형 큐의 잘못된 오버플로우 문제는 원형 큐(Circular Queue)로 해결
- `(rear + 1) % n == front`이면 Full로 판정하는 한 칸 비움 방식 사용 가능

**덱**
- addFront, addRear
- deleteFront, deleteRear
- 입력제한 덱(Input-restricted Deque): 한쪽 삽입만 허용
- 출력제한 덱(Output-restricted Deque): 한쪽 삭제만 허용

## 3. 구현 방식 비교

| 구현 | 장점 | 단점 |
|---|---|---|
| **배열 기반** | 접근 속도 빠름, 구현 단순, 캐시 친화적 | 크기 고정, 오버플로우 가능 |
| **원형 배열 기반** | 큐 공간 재사용, 버퍼 구현에 적합 | Full/Empty 판정 모호성 관리 필요 |
| **연결 리스트 기반** | 동적 크기 조절, 삽입·삭제 유연 | 포인터 오버헤드, 캐시 지역성 저하 |
| **Lock-free 구현** | 멀티스레드 고성능 큐에 적합 | ABA 문제, CAS 실패, 검증 난도 |

- 삽입·삭제 시간복잡도: 일반적으로 `O(1)`
- 탐색 시간복잡도: `O(n)`
- 공간복잡도: `O(n)`

## 4. 응용 분야

**스택**
- 함수 호출 스택, 재귀 처리
- 수식 변환 및 계산(중위 -> 후위/전위, 후위식 계산)
- 괄호 짝 검사
- 웹 브라우저 뒤로가기
- DFS(Depth-First Search), 백트래킹
- Undo/Redo 기능

**큐**
- 프로세스·작업 스케줄링(FCFS)
- 프린터 스풀링
- BFS(Breadth-First Search)
- 네트워크 패킷 버퍼링
- 메시지 큐 기반 비동기 통신
- 우선순위 큐(Priority Queue)로 확장 시 힙(Heap) 기반 구현

**덱**
- 슬라이딩 윈도우 최대값·최소값 알고리즘
- 작업 훔치기(Work-stealing) 스케줄링
- 양방향 스크롤 버퍼
- LRU 캐시 등 양방향 접근이 필요한 구조

## 5. 심화 이슈 (기술사 포인트)

1. **동시성 문제**
   - 멀티스레드 환경에서 큐·스택 접근 시 Race Condition이 발생할 수 있어 Lock-based 또는 Lock-free(CAS 기반) 설계가 필요하다.

2. **원형 큐 Full/Empty 모호성**
   - `front == rear`일 때 Empty와 Full을 구분하기 어렵기 때문에 count 변수를 두거나 한 칸을 비워두는 방식을 사용한다.

3. **우선순위 큐 확장**
   - 단순 FIFO가 아니라 우선순위 기준 처리가 필요하면 힙 기반 우선순위 큐를 사용하며 삽입·삭제는 `O(log n)`이 된다.

4. **분산 시스템에서의 큐**
   - Kafka, RabbitMQ 같은 메시지 큐는 비동기 처리, 부하 분산, 장애 격리(Decoupling)를 제공한다.

5. **캐시 지역성과 성능**
   - 고성능 네트워크 버퍼나 이벤트 큐에서는 연결 리스트보다 배열 기반 원형 버퍼가 캐시 친화적이다.

## 6. 결론

스택·큐·덱은 트리·그래프 탐색, 스케줄링, 메시징, 캐시 등 고급 알고리즘과 시스템 설계의 기초가 되는 선형 자료구조이다. 기술사 답안에서는 LIFO·FIFO·양단 접근 원리뿐 아니라 동시성 제어, 오버플로우 처리, 원형 큐 판정, 캐시 지역성까지 고려한 설계를 제시해야 한다.
