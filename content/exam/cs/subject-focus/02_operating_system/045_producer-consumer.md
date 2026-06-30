---
title: "생산자-소비자 (Producer-Consumer)"
date: "2026-06-30"
weight: 45
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 유한 버퍼(Bounded Buffer)를 공유하는 생산자와 소비자가 데이터를 주고받는 고전적 동기화 문제로, 버퍼 가득참/비어있음 조건을 동기화로 해결.

## Ⅱ. 구성요소 / 원리
- 유한 버퍼: 크기 N의 공유 큐(Queue)
- 생산자: 빈 슬롯에 데이터 삽입, 가득 차면 대기
- 소비자: 채워진 슬롯에서 제거, 비면 대기
- empty(빈 칸 수), full(찬 칸 수) 카운팅 세마포어
- mutex: 버퍼 접근 상호배제(임계구역 보호)

## Ⅲ. 흐름도 / 구조
```text
Producer:  wait(empty); wait(mutex);
           buffer 삽입;
           signal(mutex); signal(full);
Consumer:  wait(full);  wait(mutex);
           buffer 제거;
           signal(mutex); signal(empty);
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 속도 차 있는 생산/소비 주체 간 비동기 버퍼링 |
| 장점 | 결합도 감소, 처리량 평준화(Throughput Smoothing) |
| 한계 | 세마포어 순서 오류 시 교착, 버퍼 크기 튜닝 필요 |

## Ⅴ. 기술사적 적용
- wait(mutex)와 wait(empty/full) 순서 역전 시 교착 발생 → 순서 준수
- 적용: 메시지 큐(Kafka/RabbitMQ), 스레드풀 작업큐, 파이프라인
- Monitor 기반 BlockingQueue로 추상화하여 실무 구현
