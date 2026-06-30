---
title: "세마포어 (Semaphore)"
date: "2026-06-30"
weight: 43
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 정수 카운터와 원자적 연산 wait(P)/signal(V)로 자원 접근을 제어하는 동기화 도구로, 이진(Binary)·카운팅(Counting) 형태로 구분.

## Ⅱ. 구성요소 / 원리
- 정수 변수 S: 사용 가능 자원 수
- wait(P): S 감소, S<0이면 대기큐 진입(Block)
- signal(V): S 증가, 대기 스레드 깨움(Wakeup)
- P/V는 원자연산으로 수행
- 이진(0/1)=상호배제, 카운팅(N)=자원 풀 관리

## Ⅲ. 흐름도 / 구조
```text
wait(S):  S--;  if(S<0) block(self) → 대기큐
   [Critical Section / 자원 사용]
signal(S): S++; if(S<=0) wakeup(대기큐 1개)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 상호배제 및 N개 자원 동시성 제어 |
| 장점 | 카운팅 지원, 차단방식으로 CPU 절약, 신호 전달 가능 |
| 한계 | 소유권 無 → 오용 시 교착·잘못된 V로 정합성 붕괴 |

## Ⅴ. 기술사적 적용
- 비교: 이진 세마포어 ≈ Mutex(단 소유권 없음)
- 생산자-소비자: empty/full 카운팅 세마포어 + mutex 조합
- 추상화 수준 향상: Monitor(언어 차원 자동 상호배제)로 발전
