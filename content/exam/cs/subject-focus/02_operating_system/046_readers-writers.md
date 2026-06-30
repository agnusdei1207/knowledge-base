---
title: "독자-저자 (Readers-Writers)"
date: "2026-06-30"
weight: 46
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 공유데이터에 대해 다수 독자(Reader)의 동시 읽기는 허용하되, 저자(Writer)는 단독으로 배타 접근해야 하는 동기화 문제.

## Ⅱ. 구성요소 / 원리
- 독자: 데이터 읽기만, 다중 동시 접근 허용
- 저자: 데이터 변경, 단독 배타 접근 필요
- readcount: 현재 독자 수 카운트
- mutex: readcount 보호, rw_mutex: 자원 배타 접근
- 정책에 따른 기아(Starvation) 발생 가능

## Ⅲ. 흐름도 / 구조
```text
Reader:  wait(mutex); rc++;
         if(rc==1) wait(rw_mutex);   // 첫 독자가 저자 차단
         signal(mutex);
         [읽기]
         wait(mutex); rc--;
         if(rc==0) signal(rw_mutex); // 마지막 독자가 해제
         signal(mutex);
Writer:  wait(rw_mutex);[쓰기];signal(rw_mutex);
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 읽기 동시성 극대화 + 쓰기 일관성 보장 |
| 장점 | 다중 독자 병행으로 처리량 향상 |
| 한계 | 독자우선 시 저자 기아, 저자우선 시 독자 기아 |

## Ⅴ. 기술사적 적용
- 변형: 1독자우선/2저자우선/3공정(FIFO, 기아 방지)
- 구현: ReadWriteLock(Java ReentrantReadWriteLock), pthread_rwlock
- DBMS 공유락(S)/배타락(X), MVCC로 기아·경합 완화
