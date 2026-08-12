---
sidebar:
  order: 4
  label: "004. 프로세스 스케줄링 알고리즘: FCFS•SJF•RR•MLFQ•CFS (Process Scheduling)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "프로세스 스케줄링 알고리즘: FCFS•SJF•RR•MLFQ•CFS (Process Scheduling)"
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 4
extra:
  question_no: "004"
  source_status: "기출"
  source_history: "122회, 129회, 131회, 138회"
  priority: 85
  priority_note: "4회 반복, 스케줄링 기준•알고리즘 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Process Scheduling**: Ready Queue 상에 대기 중인 프로세스들에게 CPU 자원(Time Quantum/Priority)을 효율적으로 배분하는 OS 커널 스케줄링 정책.
- **Preemptive vs Non-Preemptive**: 실행 중인 프로세스의 CPU 점유권을 커널이 강제 회수(Preemptive)할 수 있는지 여부에 따른 스케줄링 구분.
- **CFS(Completely Fair Scheduler)**: Linux 커널 2.6.23부터 도입된 Red-Black Tree 기반 vruntime(가상 실행시간) 최소 프로세스를 선점 선택하는 완전 공정 스케줄러.

</details>

- 정의/개념: 시스템 응답시간, 처리량(Throughput), CPU 이용률 및 공정성을 극대화하기 위해 Ready Queue 프로세스를 선점/비선점 디스패치하는 **프로세스 스케줄링 알고리즘**
- 배경/필요성: I/O-bound 프로세스의 응답시간 보장 및 CPU-bound 프로세스의 고스루풋 연산 요구를 균형 있게 충족시키기 위한 커널 메커니즘

#### 한줄 요약

- 실행 순서와 CPU 사용시간으로 응답•처리량•공정성을 조정한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Time Quantum (Time Slice)**: Round-Robin 등 선점형 스케줄링에서 프로세스가 CPU를 한번에 점유 구동할 수 있는 허용 단위 시간.
- **Convoy Effect**: FCFS 스케줄링 시 긴 CPU 버스트 타임을 갖는 프로세스가 앞서 점유함으로써 뒤따르는 짧은 I/O 작업들이 대기 지연되는 현상.
- **Starvation**: 특정 프로세스가 우선순위에 밀려 Ready Queue에서 CPU를 영구히 할당받지 못하는 기아 현상.

</details>

- **Preemptive (RR, MLFQ, CFS)** vs **Non-preemptive (FCFS, SJF)** 스케줄링 정책 분류
- **Time Quantum** 설정에 따른 지연시간 및 컨텍스트 스위칭 오버헤드 간 트레이드오프
- 기아 현상(**Starvation**) 예방을 위한 에이징(Aging) 및 가상 실행시간(vruntime) 보정 기법 적용

#### 한줄 요약

- 시간 할당량 감소에 따른 응답 개선•전환 비용 증가한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **vruntime(Virtual Runtime)**: CFS 스케줄러에서 프로세스의 실제 실행 시간을 우선순위 가중치(Nice value)로 보정한 가상 실행 시간.
- **Red-Black Tree**: CFS 스케줄러에서 가장 작은 vruntime을 갖는 노드를 $O(\log N)$ 최저 시간 복잡도로 빠르게 탐색하기 위해 사용하는 자가 균형 이진 탐색 트리.

</details>

```text
[준비 큐]
    |
[스케줄러]
    |
[디스패처] -- [타이머]
    |
  [CPU]
```

선의 의미: Ready Queue(Red-Black Tree)에 대기 중인 프로세스를 커널 스케줄러가 평가하여 디스패처를 통해 CPU 코어로 인가하고, 하드웨어 타이머에 의해 선점 제어되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 준비 큐(Ready Queue) | FCFS(FIFO 큐), CFS(**Red-Black Tree**) 등 알고리즘별 프로세스 PCB 래칭 |
| 스케줄러 | **vruntime**, Priority, CPU Burst time에 근거하여 다음 디스패치 대상 확정 |
| 디스패처(Dispatcher) | 선택된 프로세스의 Context Restore 및 User Mode 전환 CPU 제어권 인가 |
| 타이머(Timer) | **Time Quantum** 만료 시 APIC 타이머 인터럽트를 발상하여 스케줄러 재호출 |

#### 한줄 요약

- 준비 큐, 스케줄러, 디스패처, 타이머의 CPU 배정 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Aging**: Ready Queue에서 오래 대기한 프로세스의 우선순위를 점진적으로 상승시켜 기아 현상을 방지하는 대책.

</details>

```text
┌──────────── CPU 스케줄링 반복 ────────────┐
│ 1. 준비 후보 갱신                         │
│          │                                │
│          ▼                                │
│ 2. 정책 기준 실행 대상 선택               │
│          │                                │
│          ▼                                │
│ 3. 문맥 복원•디스패치                     │
│          │                                │
│          ▼                                │
│   [실행 결과 사건]                        │
│      ┌───┴──────────┐                     │
│      │ 완료•대기    │ 할당량 만료         │
│      ▼              ▼                     │
│ [큐 이탈•대기]  4. 선점 인터럽트          │
│                     │                     │
│                     ▼                     │
│              5. 문맥 저장•재등록          │
│                     └── 준비 후보로 반복  │
└───────────────────────────────────────────┘
```

### 동작 원리

1. **준비 후보 갱신**: 신규 프로세스 인입 및 기존 대기 프로세스 우선순위 보정(**Aging** 적용).
2. **정책 기준 실행 대상 선택**: 알고리즘(CFS의 최소 **vruntime**, SJF의 최소 CPU Burst) 기반 대상 선택.
3. **문맥 복원·디스패치**: 선택된 PCB의 레지스터 복원 및 **Time Quantum** 인가.
4. **선점 인터럽트**: 하드웨어 타이머 신호에 의한 선점(Preemption) 발생 및 CPU 회수.
5. **문맥 저장·재등록**: 실행 문맥 PCB 보존 및 Ready Queue(Red-Black Tree) 재삽입.

#### 한줄 요약

- 준비 후보 갱신부터 문맥 저장·재등록까지 반복하여 스케줄링한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **MLFQ(Multi-Level Feedback Queue)**: 여러 개의 준비 큐를 두고, CPU 타임 슬라이스를 소진할 때마다 하위 큐로 강등(Demote)시키고 I/O 유발 시 상위 큐로 유지하는 자율 피드백 스케줄러.

</details>

| 스케줄링 알고리즘 | 선점 유무 | 핵심 매커니즘 | 주요 장단점 |
|:---|:---|:---|:---|
| **FCFS** | 비선점 | FIFO 큐 기반 도착 순서대로 점유 | 구현 단순 / **Convoy Effect** 발생 |
| **SJF** | 비선점/선점 | 예상 CPU Burst Time이 가장 짧은 프로세스선택 | 평균 대기시간 최적 / **Starvation** 발생 |
| **RR** | 선점형 | **Time Quantum** 기반 순환 선점 점유 | 대화형 응답성 우수 / Time Slice 튜닝 필수 |
| **MLFQ** | 선점형 | 큐별 슬라이스 차등화 및 피드백 강등/승격 | CPU/IO Bound 적응형 / 큐 튜닝 복잡성 |
| **CFS** | 선점형 | **vruntime** 최소 노드를 Red-Black Tree에서 래칭 | 완전한 공정성 / 복잡한 가중치 계산 |

#### 한줄 요약

- 짧은 작업을 알면 SJF, 빠른 교대는 RR•MLFQ, 지속적인 CPU 몫은 CFS가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Nice Value**: Linux 프로세스의 스케줄링 우선순위 가중치(-20 ~ +19 수치)로, 높을수록 CPU 점유 몫이 감소.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SJF/MLFQ 환경에서 CPU-bound 프로세스의 **Starvation** | **Aging** 기법 및 periodic queue priority boost 적용 | 기아 현상 예방 |
| RR 스케줄링 시 너무 짧은 Time Quantum으로 인한 성능 저하 | Time Quantum을 Context Switch 오버헤드의 100배 이상으로 튜닝 | CPU 유효 가용률 극대화 |
| 특정 프로세스의 독점에 따른 타 프로세스 응답성 저하 | **CFS (Nice Value)** 가중치 적용 및 vruntime 공정 스케줄링 | 시스템 공정성 보장 |

> 사례: Linux 커널 **CFS** 기반 `nice -n -10` 우선순위 제어 및 **sysctl sched_latency_ns** 튜닝

#### 한줄 요약

- 혼합 서비스의 작업 클래스와 CPU 가중치를 분리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스케줄링 알고리즘 선택 기준(Process Scheduling Selection Criteria)**: 워크로드 특성(Interactive vs Batch), 응답시간 타깃, 공정성 요구에 따른 최적 스케줄러 체계.

</details>

- **스케줄링 알고리즘 선택 기준**에 따라 범용 OS 환경에는 **Linux CFS / MLFQ**, 리얼타임 제어 환경에는 **RTOS EDF/RM** 채택

#### 한줄 요약

- 버스트 예측, 응답 목표, CPU 몫에 따라 정책을 선택한다.
