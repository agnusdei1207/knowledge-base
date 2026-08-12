---
sidebar:
  order: 2
  label: "002. PCB•컨텍스트 스위칭 (PCB Context Switching)"
  badge:
    text: "기출 • 50%"
    variant: note
title: PCB•컨텍스트 스위칭 (PCB Context Switching)
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 2
extra:
  question_no: "002"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 문맥 전환 비용•PCB 상태 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **PCB(Process Control Block)**: OS 커널이 특정 프로세스의 PID, 상태, PC, CPU 레지스터, 가상 메모리 매핑 및 개방 디스크립터를 관리하는 커널 핵심 자료구조.
- **Context Switching**: 인터럽트나 시스템 콜 발생 시, 현재 CPU 상에서 구동 중인 프로세스/스레드의 레지스터 문맥(Context)을 PCB/TCB에 백업하고 신규 대상 문맥을 복원(Restore)하는 제어 전환 기법.
- **TCB(Thread Control Block)**: 스레드 단위 스케줄링 시 TID, 레지스터 상태, PC, SP 및 우선순위 정보를 독립적으로 보관하는 스레드 제어 블록.

</details>

- 정의/개념: CPU 하드웨어 자원을 복수의 실행 주체가 선점 공유하기 위해 레지스터 및 가상 메모리 상태를 **PCB & TCB**에 보존/복원하는 **컨텍스트 스위칭(Context Switching)**
- 배경/필요성: 단일/다중 코어 상에서 멀티태스킹(Multitasking) 및 타임 셰어링(Time-sharing) 구동 시 중단 시점의 실행 상태를 완전 복원하기 위한 필수 메커니즘

#### 한줄 요약

- 현재 문맥 저장과 다음 문맥 복원으로 실행 주체를 교체한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **CR3 Register**: x86 아키텍처 상에서 현재 프로세스의 최상위 페이지 테이블(PGD) 가상 주소를 가리키는 레지스터로, 프로세스 간 문맥 전환 시 교체 인가.
- **TLB Miss/Invalidation**: 프로세스 문맥 전환 시 MMU CR3 변경으로 기존 TLB 캐시가 무효화되어 발생되는 메모리 주소 번역 지연 현상.
- **Cache Locality Loss**: 문맥 전환으로 인해 CPU L1/L2/L3 캐시 상의 기존 데이터가 쫓겨나고 신규 프로세스 데이터로 교체(Cache Pollution)되어 성능이 저하되는 현상.

</details>

- CPU 레지스터, PC, SP 및 MMU 레지스터(**CR3**)를 커널 메모리(**PCB/TCB**)에 보존
- 프로세스 간 전환 시 **TLB Flush** 및 **Cache Locality Loss** 발생으로 인한 물리적 성능 오버헤드
- 스레드 간 전환 시 주소 공간 공유로 인해 TLB 무효화 없이 초고속 레지스터 덤프/복원만 수행

#### 한줄 요약

- 응답성 향상과 문맥 전환 비용 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **PCB 구조체**: PID, Process State, Program Counter, CPU Registers, Memory Limits, Open File Descriptors, I/O Status.
- **Kernel Stack**: 프로세스/스레드가 커널 모드로 진입 시 레지스터 상태 및 문맥을 덤프 보관하는 커널 공간 내의 전용 스택 영역.

</details>

```text
[CPU]
  |
  |
+----------------------- [운영체제 커널] -----------------------+
|                              |                                |
|                        [스케줄러]                             |
|                         /        \                            |
|                        /          \                           |
|                 [PCB 저장부]   [TCB 저장부]                  |
+---------------------------------------------------------------+
```

선의 의미: CPU 실행 레지스터가 커널 스케줄러의 타임 슬라이스(Time Quantum) 만료 시 PCB/TCB 저장부로 덤프되고 신규 문맥이 인가되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| CPU 레지스터 | PC, SP, General Registers 등 현재 구동 중인 레지스터 값 상주 |
| 커널 스케줄러 | **Timer Interrupt** 수용, **PCB/TCB** 참조 및 다음 디스패치 대상 선정 |
| PCB 저장부 | 가상 메모리 테이블(CR3), 파일 디스크립터, 프로세스 상태(Ready/Running/Block) 저장 |
| TCB 저장부 | 스레드 전용 Stack Pointer, Register, Priority 메타데이터 보관 |
| Kernel Stack | 인터럽트 발생 즉시 하드웨어 레지스터 프레임을 조용히 덤프 기록하는 영역 |

#### 한줄 요약

- 운영체제 커널, 스케줄러, PCB 저장부, TCB 저장부 기반 문맥 전환 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Timer Interrupt**: APIC/PIT 하드웨어에 의해 일정 주기(예: 1ms)마다 발생하여 커널 스케줄러를 호출하는 하드웨어 타이머 신호.

</details>

```text
[선점 인터럽트•대기 발생]
            │
            ▼
1. 현재 실행 문맥 저장
            │
            ▼
2. 런 큐 정책 평가
            │
            ▼
3. 다음 PCB•TCB 선택
            │
      ┌─────┴──────────┐
      │ 동일 프로세스 │ 다른 프로세스
      │                ▼
      │        4. 주소 공간 전환
      └────────┬───────┘
               ▼
5. 문맥 복원•디스패치
               │
               ▼
        [CPU 실행 재개]
```

### 동작 원리

1. **현재 실행 문맥 저장**: **Timer Interrupt** 또는 I/O Block 발생 시 CPU 레지스터를 현재 **TCB/PCB** 및 **Kernel Stack**에 저장.
2. **런 큐 정책 평가**: OS 커널 스케줄러가 Run-Queue 내 우선순위(CFS vruntime 등) 평가.
3. **다음 PCB·TCB 선택**: 디스패치할 신규 스레드/프로세스 선정.
4. **주소 공간 전환**: 프로세스 변경 시 **CR3** 레지스터 갱신 (**TLB Flush** 인가).
5. **문맥 복원·디스패치**: 신규 TCB의 PC, SP 및 레지스터 세트를 복원하고 사용자 모드(User Mode) 복귀 실행.

#### 한줄 요약

- 현재 실행 문맥 저장, 런 큐 정책 평가, 다음 PCB·TCB 선택, 주소 공간 전환, 문맥 복원·디스패치를 순서대로 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Process Context Switch vs Thread Context Switch**: MMU 주소 공간(CR3) 교체 및 TLB Flush 수반 유무에 따른 오버헤드 차이.

</details>

| 비교 항목 | Process Context Switch | Thread Context Switch |
|:---|:---|:---|
| MMU 주소 공간 | 주소 공간 교체 필수 (**CR3 레지스터 갱신**) | 주소 공간 완전 공유 (**CR3 교체 없음**) |
| TLB 영향 | **TLB Flush** 발생 (메모리 억세스 지연 증가) | **TLB Flush** 미발생 (TLB 캐시 유연 유지) |
| 오버헤드 크기 | 큼 (~수 μs 수치, Cache Pollution 유발) | 작음 (~수백 ns 수치, 레지스터 복원만 수행) |
| 보존 대상 | **PCB** (Process State, MMU Table, File Descriptors) | **TCB** (Stack Pointer, Program Counter, Registers) |

#### 한줄 요약

- 프로세스는 주소 공간까지, 스레드는 실행 문맥만 전환한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **CPU Pinning (Affinity)**: 프로세스/스레드를 특정 CPU 코어에 고정하여 컨텍스트 스위칭 시 캐시 적중률(Cache Locality)을 보장하는 기법.

</details>

| 문제 | 대책 | 과실 효과 |
|:---|:---|:---|
| 과도한 타임 슬라이스 세분화로 인한 **Context Switch** 오버헤드 폭증 | Time Quantum 최적화 (sysctl **sched_min_granularity_ns**) | CPU 가용률 및 스루풋 확보 |
| 코어 간 스레드 핑퐁 이동에 따른 **Cache Locality Loss** | **CPU Affinity (sched_setaffinity)** 설정 | L1/L2 캐시 히트율 상향 |
| 프로세스 수 폭증으로 인한 **TLB Flush** 대기 지연 | 스레드 기반 아키텍처 또는 **Async I/O (epoll/io_uring)** 전환 | 가상 메모리 변환 오버헤드 소멸 |

> 사례: Linux 커널 **CFS(Completely Fair Scheduler)** 튜닝 및 **taskset** 기반 CPU Pinning 최적화

#### 한줄 요약

- 응답 목표와 전환 비중을 함께 반영해 시간 할당량을 조정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **컨텍스트 스위칭 선택 기준(Context Switching Optimization Criteria)**: 타임 슬라이스 주기, 스레드 멀티태스킹 비율 및 TLB 오버헤드 제어에 기초한 시스템 수립 체계.

</details>

- **컨텍스트 스위칭 선택 기준**에 따라 초고성능 트랜잭션 시스템은 **Thread Context Switch** 및 **Async Non-blocking I/O** 기반 구조 채택

#### 한줄 요약

- 응답 지연과 전환 비중에 따라 시간 할당량을 조정한다.
