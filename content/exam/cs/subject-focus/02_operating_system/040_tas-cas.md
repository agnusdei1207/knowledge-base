---
title: "TAS·CAS (Test-And-Set / Compare-And-Swap)"
date: "2026-06-30"
weight: 40
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 메모리 읽기-수정-쓰기를 단일 명령으로 수행하는 원자적(Atomic) 하드웨어 명령으로, 상호배제 락(Lock) 구현의 기반.

## Ⅱ. 구성요소 / 원리
- TAS(Test-And-Set): 변수를 true로 설정하고 이전 값을 반환(원자적)
- CAS(Compare-And-Swap): 기대값과 일치 시에만 새 값으로 교체, 성공/실패 반환
- 원자성: 명령 실행 중 인터럽트·선점 불가, 버스 락(Bus Lock)으로 보장
- CAS는 무잠금(Lock-free) 자료구조의 핵심 프리미티브
- ABA 문제: 값이 A→B→A로 복귀 시 변화 미감지(버전 태그로 해결)

## Ⅲ. 흐름도 / 구조
```text
[TAS Lock]                  [CAS]
while(TestAndSet(lock))     do {
      ;  // spin              old = *p;
[Critical Section]            new = f(old);
lock = false;               } while(!CAS(p, old, new));
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | HW 원자명령으로 효율적 상호배제 구현 |
| 장점 | 단순·고속, 멀티코어 확장성, Lock-free 가능 |
| 한계 | Busy Waiting, 한정대기 미보장, CAS는 ABA 문제 |

## Ⅴ. 기술사적 적용
- Mutex/Spinlock의 내부 구현 명령
- CAS 기반 원자연산: Java AtomicInteger, C++ std::atomic
- 비교: TAS=단순 락 / CAS=조건부 교체, Lock-free 알고리즘 토대
