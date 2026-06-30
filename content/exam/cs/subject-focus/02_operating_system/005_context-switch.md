---
title: "문맥교환 (Context Switch)"
date: "2026-06-30"
weight: 5
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 문맥교환(Context Switch)은 CPU가 실행 중인 프로세스(또는 스레드)를 다른 프로세스로 전환하기 위해 현재 프로세스의 문맥을 프로세스 제어 블록(PCB, Process Control Block)에 저장하고 다음 프로세스의 문맥을 복원하는 과정이다.

## Ⅱ. 구성요소 / 원리
- **PCB(Process Control Block)**: 프로그램 카운터(PC), 레지스터, 상태, 메모리 정보 저장 구조
- **문맥 저장(Save)**: 현재 프로세스의 CPU 레지스터·PC를 PCB에 저장
- **문맥 복원(Restore)**: 다음 프로세스의 PCB에서 레지스터·PC를 CPU에 적재
- **발생 시점**: 타이머 인터럽트(선점), I/O 대기, 시스템콜, 우선순위 변동
- **TLB 플러시(Flush)**: 주소공간 변경 시 TLB(Translation Lookaside Buffer) 무효화

## Ⅲ. 흐름도 / 구조
```text
[프로세스 A 실행]
   │ 인터럽트/스케줄러 호출
   ▼
A 문맥 → PCB(A)에 저장
   │
   ▼  (주소공간 변경 시 TLB flush)
PCB(B)에서 문맥 복원 → CPU 적재
   │
   ▼
[프로세스 B 실행]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 멀티태스킹·시분할을 위한 CPU 자원의 프로세스 간 전환 |
| 장점 | 동시성·응답성 확보, 자원 활용률 향상 |
| 한계 | 저장/복원·TLB/캐시 플러시로 인한 순수 오버헤드(생산성 0) |

## Ⅴ. 기술사적 적용
- 스레드 문맥교환은 주소공간 공유로 프로세스 대비 오버헤드 작음
- 잦은 문맥교환(Context Switch Thrashing) 방지를 위한 스케줄링 튜닝
- CPU 친화도(Affinity)·코어 고정으로 캐시·TLB 미스 최소화
