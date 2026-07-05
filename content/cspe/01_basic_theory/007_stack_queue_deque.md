---
title: 스택·큐·덱 (Stack Queue Deque)
date: 2026-07-05
tags: ["cspe-basic_theory"]
weight: 007
---

## Ⅰ. 개요
- 데이터의 삽입과 삭제 위치가 제한된 선형 자료구조들임.
- LIFO, FIFO 등 고유의 접근 방식을 통해 특정 알고리즘의 기반이 됨.
- [표] 출제 의도: 자료구조별 동작 특성 이해 및 적소 활용 능력 평가.

## Ⅱ. 구성요소
- ASCII 구조도
  Stack: [ Top ]   Queue: [ Front |...| Rear ]   Deque: [ L |...| R ]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Stack | 후입선출 (LIFO, Last-In First-Out) | 프링글스 통 |
| Queue | 선입선출 (FIFO, First-In First-Out) | 맛집 대기줄 |
| Deque | 양쪽 끝에서 입출력 가능 (Double-ended) | 양방향 터널 |

> 요약: 입출력 규칙에 따라 데이터 흐름을 제어함.

## Ⅲ. 절차
- ASCII 흐름도
  Push/Enqueue -> Check Full -> Insert -> Pop/Dequeue -> Check Empty

1. 연산 종류(삽입/삭제)와 위치(Top/Rear/Front)를 지정함.
2. 자료구조의 포화(Full) 또는 공백(Empty) 상태를 체크함.
3. 포인터(Top, Front, Rear)를 이동시키며 데이터를 처리함.
4. 처리된 결과를 반환하고 상태 정보를 갱신함.

> 요약: 포인터 조작을 통해 정해진 규칙대로 데이터를 관리함.

## Ⅳ. 문제점
- 일반 큐는 삭제 시 데이터 이동이 필요하거나 빈 공간 낭비 발생함.
- 정적 배열 구현 시 크기 확장이 어렵고 메모리 오버플로우 위험함.

## Ⅴ. 개선방안
- 단기: 원형 큐(Circular Queue) 도입으로 메모리 재사용 극대화함.
- 중기: 연결 리스트 기반 구현으로 동적 크기 확장성 확보함.
- 장기: 우선순위 큐(Priority Queue) 적용으로 실행 우선순위 제어함.

## Ⅵ. 전망
- 초고속 데이터 처리를 위해 복사 오버헤드를 제거한 제로 카피(Zero-copy) 큐와 RDMA 기술의 결합이 차세대 네트워크 인프라의 핵심 기술이 될 것임.
- 고주파 매매(HFT)와 같이 지연 시간에 민감한 분야에서 LMAX Disruptor 패턴과 같은 링 버퍼 기반의 고성능 큐가 시스템 경쟁력의 CSF로 작용할 것임.
- 함수형 프로그래밍 언어의 확산에 따라 불변성(Immutability)을 보장하면서도 효율적인 영속적 자료구조(Persistent Data Structure) 형태의 스택/큐가 보편화될 전망임.
