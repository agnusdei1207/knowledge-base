---
title: "[핵심] CPU 스케줄링 종합 (CPU Scheduling)"
date: "2026-06-30"
weight: 78
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 준비 큐(Ready Queue)에 있는 여러 프로세스 중 다음에 CPU(Central Processing Unit, 중앙처리장치)를 할당할 프로세스를 선택하는 운영체제의 자원 분배 기법으로, 처리율·응답시간·공정성·기아 방지를 목표로 한다.

## Ⅱ. 구성요소 / 원리
- 선점형(Preemptive): 실행 중 프로세스의 CPU를 강제 회수(RR, SRT, EDF), 비선점형(Non-preemptive): 자발 반납까지 점유(FCFS, SJF)
- FCFS(First-Come First-Served, 선입선처리): 도착순 처리, 긴 작업이 앞서면 호위효과(Convoy Effect) 발생
- SJF(Shortest Job First, 최단작업우선): 실행시간 최소부터 처리, 평균 대기시간 최소(이론상 최적)이나 기아 발생
- RR(Round Robin, 라운드로빈): 타임 퀀텀(Time Quantum) 단위 순환, 시분할(Time Sharing) 응답성 보장
- 실시간(Real-Time): RM(Rate Monotonic, 정적 우선순위)·EDF(Earliest Deadline First, 동적 마감우선)

## Ⅲ. 흐름도 / 구조
```text
[New]→[Ready Queue]──(Dispatch)──→[Running]──(I/O)──→[Waiting]
          ↑  ↑                        │                  │
          │  └──(선점/Time Quantum 만료)─┘                  │
          └────────────(I/O 완료)──────────────────────────┘
   기아(Starvation) 발생 시 → Aging(대기시간 비례 우선순위 상향)으로 해소
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | FCFS=단순·공정 / SJF=평균대기 최소 / RR=응답성 / RM·EDF=마감시간 보장 |
| 장점 | 선점형은 응답성·실시간성 우수, SJF는 처리율 최대, EDF는 동적 마감 100% 활용 |
| 한계 | FCFS=호위효과, SJF=기아·실행시간 예측난, RR=퀀텀 의존(작으면 오버헤드 큼) |

## Ⅴ. 기술사적 적용
- 기아 문제는 Aging 기법으로 대기시간에 비례해 우선순위를 점진 상향시켜 해결
- 실시간 시스템은 경성(Hard)=EDF/RM, 연성(Soft)=우선순위 기반으로 분리 설계
- 다단계 피드백 큐(MLFQ)로 FCFS·SJF·RR 장점을 통합한 적응형 스케줄링 구현
