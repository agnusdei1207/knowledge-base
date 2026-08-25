---
sidebar:
  order: 3
  label: "003. 프로세스 생성•종료•상태 전이"
  badge:
    text: "미출 · 30%"
    variant: note
title: "프로세스 생성•종료•상태 전이 (Process Lifecycle)"
date: "2026-08-25T10:45:00+09:00"
tags: [notes-software]
weight: 3
extra:
  question_no: "003"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "프로세스 상태 전이는 운영체제 기본 흐름"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **프로세스 생명주기(Process Lifecycle)**: 프로세스가 생성(New)되어 준비(Ready), 실행(Running), 대기(Blocked), 종료(Terminated) 상태를 거치며 자원을 점유 및 반납하는 주기.
- **fork() / exec()**: 부모 프로세스의 주소 공간을 복제(fork)하여 자식을 만들고 새로운 바이너리로 교체(exec) 실행하는 시스템 콜.

</details>

- 정의/개념: 프로세스가 생성부터 준비, 실행, 대기, 종료 상태를 능동적으로 전이하며 커널 자원을 제어받는 **프로세스 생명주기** 관리 기제
- 배경/필요성: 단일 실행 구조로는 **CPU 연산과 I/O 대기 작업 간의 시분할 다중화 및 자원 활용률 극대화 불가**

#### 한줄 요약
- 커널이 프로세스 상태를 5단계로 통제하여 CPU와 I/O 자원을 최적 다중화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **디스패치(Dispatch)**: 준비 큐의 최우선 프로세스를 선택하여 CPU 제어권을 부여하고 실행 상태로 전이시키는 동작.
- **좀비 프로세스(Zombie Process)**: 자식 프로세스가 종료되었으나 부모가 wait()으로 종료 상태를 회수하지 않아 PID 테이블에 잔존하는 상태.

</details>

- 단일 CPU 코어 기준 **실행 상태(Running)** 는 시점당 단 하나의 프로세스에만 배정
- 준비 큐(Ready Queue)와 외부 I/O 대기 큐(Wait Queue)의 **큐 이원화** 분리 운영
- 부모 프로세스의 `wait()` 시스템 콜을 통한 자식 PCB 회수 및 **좀비 프로세스** 방지

#### 한줄 요약
- 5단계 상태 분리와 큐 이원화를 통해 CPU 선점과 I/O 이벤트를 처리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **준비 큐(Ready Queue)**: 메모리에 적재되어 CPU 할당을 기다리는 프로세스 PCB의 연결 리스트.
- **대기 큐(Wait Queue)**: I/O 완료 또는 동기화 이벤트를 대기하는 프로세스 PCB의 연결 리스트.

</details>

```text
[프로세스 상태 전이 및 큐 아키텍처]
|-- 프로세스 생성 (New: fork/exec 시스템 콜)
|-- 준비 큐 (Ready Queue - CPU 할당 대기 PCB 리스트)
|   `-- 스케줄러 디스패치 (Dispatch) -> CPU 코어 실행 (Running)
|-- 타이머 만료 선점 (Timeout/Preempt) -> 준비 큐 복귀
|-- I/O 및 이벤트 대기 (Block) -> 대기 큐 (Wait Queue)
|   `-- I/O 완료 인터럽트 (Wakeup) -> 준비 큐 복귀
`-- 프로세스 종료 (Terminated: exit/wait 자원 해제)
```

선의 의미: 계층 및 상태 전이 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| **프로세스 제어 블록(PCB)** | PID, 프로세스 상태(Ready/Running/Blocked), CPU 레지스터 저장 |
| **준비 큐(Ready Queue)** | 스케줄링 정책에 따라 CPU 할당을 대기 중인 PCB 연결 리스트 관리 |
| 커널 스케줄러 | 준비 큐에서 최적 프로세스를 선택하여 CPU 제어권을 이양(Dispatch) |
| **대기 큐(Wait Queue)** | 디스크/네트워크 I/O 완료 또는 시그널을 기다리는 PCB 격리 관리 |
| init / systemd (PID 1) | 부모 잃은 고아 프로세스를 입양하여 자원 누출 방지 |

#### 한줄 요약
- PCB, 준비 큐, 대기 큐, 커널 스케줄러가 결합되어 프로세스 상태 전이를 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **선점(Preemption)**: 타임 퀀텀 만료 또는 고우선순위 프로세스 등장 시 실행 중인 CPU를 강제 회수하는 동작.

</details>

```text
프로세스 생성 요청 (fork/exec: New 상태)
        │
   메모리 승인 후 준비 큐 진입 (Ready 상태)
        │
   스케줄러가 디스패치(Dispatch)하여 CPU 할당
        │
   명령어 실행 중 (Running 상태)
   ┌────┴───────────────────────────┐
타임아웃(선점)    I/O 요청 발생       실행 완료 (exit)
   │                  │                  │
준비 큐 복귀      대기 큐로 전이      종료 상태 (Terminated)
(Ready)          (Blocked 상태)          │
   ▲                  │             부모가 wait() 호출하여
   │             I/O 완료 인터럽트   자원 및 PCB 완전 해제
   └──────────────────┘ (Wakeup)
```

#### 한줄 요약
- 생성 → 준비 → 실행 → 선점 복귀 또는 I/O 대기 후 복귀 → 종료 자원 회수 순으로 전이된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **고아 프로세스(Orphan Process)**: 부모가 먼저 종료되어 PID 1(init/systemd) 프로세스에 입양되는 프로세스.

</details>

| 프로세스 상태 | 준비 상태 (Ready) | 실행 상태 (Running) | 대기 상태 (Blocked) |
|:---|:---|:---|:---|
| CPU 점유 여부 | 미점유 (스케줄러 디스패치 대기) | **점유 중** (명령어 파이프라인 실행) | 미점유 (이벤트 대기 중) |
| 상주 큐 위치 | **준비 큐 (Ready Queue)** | CPU 코어 레지스터 | **대기 큐 (Wait Queue)** |
| 다음 전이 경로 | **실행 (Running)** (디스패치 시) | **준비** (선점) / **대기** (I/O) | **준비 (Ready)** (I/O 완료 시) |
| 스케줄러 개입 | 스케줄링 알고리즘에 의해 선택됨 | 타이머 인터럽트로 강제 선점됨 | 스케줄러 선택 대상에서 제외됨 |

#### 한줄 요약
- 준비는 CPU를 기다리고, 실행은 연산하며, 대기는 I/O 완료 후 준비 상태로 복귀한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **waitpid()**: 자식 프로세스의 종료 상태를 감시하고 자원을 비동기로 회수하는 시스템 콜.
- **ulimit(User Limit)**: 단일 사용자 또는 프로세스가 생성할 수 있는 최대 프로세스 수(nproc)를 제한하는 커널 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자식 종료 상태 미회수로 **좀비 프로세스 누적** 및 PID 고갈 | `SIGCHLD` 핸들러 등록 및 **`waitpid(..., WNOHANG)` 비동기 회수** | 커널 PCB 테이블 즉시 정리 및 PID 자원 고갈 방지 |
| 외부 I/O 지연으로 인한 프로세스 대기 상태(Blocked) 무한 누적 | 소켓 및 디스크 I/O 시 **Non-blocking I/O 및 Timeout** 설정 | 무한 블로킹 방지 및 시스템 가용성 유지 |
| 프로세스 무한 포크 공격(Fork Bomb) 시스템 마비 | `/etc/security/limits.conf` 내 **`nproc` 제한(ulimit)** 설정 | 프로세스 폭증 차단 및 OS 전체 가용성 확보 |
| 부모 비정상 종료로 인한 고아 프로세스 잔존 | PID 1(`init/systemd`)의 자동 입양 및 종료 자원 회수 보장 | 메모리 및 파일 디스크립터 누수 방지 |

#### 한줄 요약
- waitpid 비동기 회수, I/O 타임아웃, ulimit 프로세스 수 제한으로 안정성을 보장한다.

## Ⅶ. 결론

- 클라우드 및 컨테이너 런타임 환경에서 **안정적인 프로세스 생명주기 관리(PID 1 reaping, 타임아웃, cgroups 프로세스 한도 통제)** 필수 적용

#### 한줄 요약
- 프로세스 생명주기 통제는 시스템 자원 누수를 막고 고가용성 멀티태스킹을 보장하는 운영체제의 근간이다.