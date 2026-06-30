---
title: "[핵심] 세마포어·동기화 종합 (Semaphore & Synchronization)"
date: "2026-06-30"
weight: 81
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 공유자원에 대한 동시 접근을 제어하여 경쟁상태(Race Condition)를 방지하는 프로세스 동기화 기법으로, 세마포어는 정수 변수와 원자적 연산 wait(P)·signal(V)로 임계구역을 보호한다.

## Ⅱ. 구성요소 / 원리
- 임계구역(Critical Section) 3조건: 상호배제(Mutual Exclusion)·진행(Progress)·한정대기(Bounded Waiting)
- 이진 세마포어(Binary Semaphore): 0/1 값, 상호배제 락(Mutex) 역할
- 카운팅 세마포어(Counting Semaphore): 가용 자원 개수 표현, 다중 인스턴스 제어
- wait(P): 자원 감소·음수면 블록, signal(V): 자원 증가·대기 프로세스 깨움 (원자적 연산)
- 모니터(Monitor): 공유데이터+프로시저 캡슐화, 컴파일러가 상호배제 자동 보장

## Ⅲ. 흐름도 / 구조
```text
        wait(S):  S = S - 1
                  if (S < 0) → 프로세스 블록(대기 큐 삽입)
   ┌─────────────[ 임계구역(Critical Section) ]─────────────┐
        signal(S): S = S + 1
                  if (S <= 0) → 대기 프로세스 1개 깨움(wakeup)
   우선순위 역전(Priority Inversion) → 우선순위 상속(Inheritance)으로 해소
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 상호배제 보장과 자원 동기화로 경쟁상태·데이터 불일치 방지 |
| 장점 | 세마포어=경량·범용, 모니터=고수준 추상화로 사용오류↓, 자동 상호배제 |
| 한계 | 세마포어=P/V 순서오류 시 교착·기아, 우선순위 역전 발생 가능 |

## Ⅴ. 기술사적 적용
- wait(P)/signal(V)는 반드시 원자적 연산으로 구현(인터럽트 비활성·TestAndSet 등 하드웨어 지원)
- 모니터는 조건변수(Condition Variable)의 wait/signal로 임계구역 진입을 자동 상호배제 제어
- 우선순위 역전은 낮은 우선순위 작업에 일시적으로 우선순위를 상속(Priority Inheritance)시켜 해결
